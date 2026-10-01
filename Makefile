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

include $(TOPDIR)/feeds/luci/luci.mk

# call BuildPackage - OpenWrt buildroot signature
