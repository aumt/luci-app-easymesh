#!/usr/bin/env python3
"""生成 `make package/luci-app-easymesh/compile` 的**先决条件**覆盖值。

## 背景：为什么需要覆盖先决条件

本包是纯 Lua 包（`PKGARCH:=all`，无 `src/Makefile`），但它声明的运行时依赖
（`kmod-batman-adv` / `kmod-cfg80211` / `batctl-default` / `dawn` / `luci-compat` /
`luci-proto-batman-adv` / `libiwinfo-lua` / `bash` …）都是 `DEPENDS:=+foo`，
会被编成 kconfig 的 `select`。于是 `make package/luci-app-easymesh/compile`
会顺着 `tmp/.packagedeps` 里的这一行：

    $(curdir)/luci-app-easymesh/compile += $(curdir)/feeds/base/iwinfo/compile \
        $(curdir)/feeds/base/mac80211/compile $(curdir)/feeds/packages/dawn/compile ...

把 mac80211 / hostapd / batman-adv / batctl / dawn / iwinfo / **linux-firmware
（582MB 下载）** 整套编一遍。对一个 noarch 的 Lua 包毫无必要：产物内容和
apk/ipk 里的 `depends` 元数据都不受影响（元数据来自 Makefile 的 `LUCI_DEPENDS`）。

## 为什么不能靠改 tmp/.packagedeps

`include/toplevel.mk` 里是 `prepare-tmpinfo: FORCE`，每次 make 都会重新生成
`tmp/.packagedeps`，所以改文件必被覆盖（实测确认）。

## 正确的杠杆

`include/subdir.mk:74` 用**与目标同名**的变量当先决条件：

    $(1)/$(bd)/$(target): $(if $(NO_DEPS)$(QUILT),,$($(1)/$(bd)/$(target)) ...)

而 GNU make 里命令行赋值的变量会压掉 makefile 里的 `+=`。所以在命令行上把
`package/luci-app-easymesh/compile` 重新赋值，就换掉了先决条件。

## 保留什么

只保留 host 工具与 toolchain —— i18n 打包要用 `luci-base` 提供的 `po2lmo`。

**条件依赖必须连同 `$(if ...)` 守卫一起保留**，形如：

    $(if $(CONFIG_LUCI_CSSTIDY),$(curdir)/feeds/luci/csstidy/host/compile)

这些来自 `luci.mk:116` 的 `PKG_BUILD_DEPENDS += ... LUCI_CSSTIDY:csstidy/host
LUCI_SRCDIET:luasrcdiet/host`。剥掉守卫会把本该跳过的包强行编出来 ——
`luasrcdiet` 要联网下 `sources.cdn.openwrt.org` 的 tarball。

用法: gen-keep.py <sdk/tmp/.packagedeps> <sdk/.config>
输出: 一行以空格分隔的先决条件（`$(curdir)` 已展开为 `package`）
"""
import re
import sys

MARKER = "$(curdir)/luci-app-easymesh/compile +="


def split_top_level(s):
    """按括号深度切词，保证 $(if ...) 这类整组不会被空格拆开。"""
    toks, buf, depth = [], "", 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch.isspace() and depth == 0:
            if buf:
                toks.append(buf)
                buf = ""
        else:
            buf += ch
    if buf:
        toks.append(buf)
    return toks


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip().splitlines()[-2])
    packagedeps, dotconfig = sys.argv[1], sys.argv[2]

    line = next((l for l in open(packagedeps, encoding="utf-8")
                 if l.startswith(MARKER)), None)
    if line is None:
        sys.exit("找不到依赖行: " + MARKER)
    body = line[len(MARKER):].strip()

    enabled = set()
    for l in open(dotconfig, encoding="utf-8"):
        l = l.strip()
        # 存带 CONFIG_ 前缀的完整符号名 —— 守卫里写的也是带前缀的
        # $(if $(CONFIG_LUCI_CSSTIDY),...) ，两边口径必须一致
        if l.startswith("CONFIG_") and l.endswith("=y"):
            enabled.add(l[:-2])

    keep, dropped = [], []
    for tok in split_top_level(body):
        m = re.match(r"^\$\(if \$\((\w+)\),(.+)\)$", tok)
        guard, inner = (m.group(1), m.group(2)) if m else (None, tok)
        if not re.search(r"/host/compile$|/toolchain/compile$", inner):
            continue
        if guard and guard not in enabled:
            dropped.append((inner, guard))
            continue
        keep.append(tok)

    if not keep:
        sys.exit("保留列表为空，依赖行格式可能变了")

    for inner, guard in dropped:
        sys.stderr.write("  (跳过 %s：%s 未启用)\n" % (inner, guard))
    print(" ".join(keep).replace("$(curdir)", "package"))


if __name__ == "__main__":
    main()
