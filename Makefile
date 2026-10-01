#
#-- TorGuard
#
#--Add +wpad-mesh-openssl or wpa package for build

include $(TOPDIR)/rules.mk

PKG_NAME:=luci-app-easymesh
PKG_VERSION:=3.8.17
# AUTORELEASE 在 apk 时代已被 OpenWrt 标记废弃（编译时会打 DEPRECATION NOTICE），改用固定序号
PKG_RELEASE:=1
PKG_MAINTAINER:=TorGuard <admin@torguard.net>

LUCI_TITLE:=LuCI Support for easymesh
# luci-lua-runtime 由 luci.mk 依据 luasrc/ 的存在自动加入，无需在此重复声明
LUCI_DEPENDS:= +kmod-cfg80211 +batctl-default +kmod-batman-adv +dawn +luci-compat +bash +libiwinfo-lua +luci-proto-batman-adv

# luci.mk 里翻译包 luci-i18n-* 的版本号取 PKG_PO_VERSION，主包用的 LUCI_VERSION 取
# PKG_SRC_VERSION，两者都由 findrev 推导。findrev 的启发式是「在 git 仓库里就查本目录
# 最近一次提交、不在 git 仓库里就按文件 mtime 兜底」，它漏了第三种状态：有 git、但文件
# 不在 git 里 —— CI 里本包正是被 rsync 进 SDK 的未跟踪副本（检出根有 .git，而
# sdk/package/luci-app-easymesh 没有任何历史），于是 git log 成功却查不到东西，版本号
# 被静默推成 "0"；本地构建树没有 .git，反而走 mtime 分支得到 0.<日期>.<秒>。同一份代码
# 两边编出不同版本号，且 CI 侧恒为 0。这里固定成主包版本，让两边一致。
# （两个变量在 luci.mk 里都是 ?=，先定义即生效）
PKG_PO_VERSION:=$(PKG_VERSION)
PKG_SRC_VERSION:=$(PKG_VERSION)

include $(TOPDIR)/feeds/luci/luci.mk

# call BuildPackage - OpenWrt buildroot signature
