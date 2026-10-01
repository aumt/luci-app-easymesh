# **📶OpenWRT EasyMesh WiFi App**  

### **Deploy a Mesh WiFi Network in Minutes with OpenWRT & Batman-adv**  

This app was created to make it **faster and easier** to deploy a **basic mesh WiFi network** for WireGuard using OpenWRT and **batman-adv**. The app is powered by **Batman-adv (Better Approach To Mobile Adhoc Networking - Advanced)** and is designed for **seamless integration with TorGuard’s WireGuard apps**. However, it can also be used **standalone** without a VPN.  

### **Why Use a Mesh WiFi Network?**  
Mesh WiFi networks are ideal for:  
✔ **Extending VPN WiFi coverage** over large areas  
✔ **Enhancing connectivity** using multiple nodes over WiFi or Ethernet  
✔ **Improving performance** by enabling seamless roaming  
✔ **Simplifying homelab setups** behind WireGuard for managing devices across locations  

---

## **🔥 Features**  

- **Easy server deployment** for access point WiFi and backhaul mesh networks  
- **Supports WPA3 authentication** (or open networks)  
- **Advanced settings**: K/V/R, Mobility Domain, RSSI Threshold  
- **Mesh status dashboard** showing Interface, Neighbor Nodes, and Last Seen time  
- **Client/Node support** for DHCP or Static IP & Dumb AP mode  
- **Auto Firewall & Interface Configuration** for Mesh Servers and Clients  
- **Dumb AP Mesh Nodes** can provide Internet access via LAN ports  
- **Compatible with TorGuard's WireGuard OpenWRT App** for VPN-based mesh networks  

---

# **📦 How to Compile & Install `luci-app-easymesh` Using OpenWRT SDK**  

### **Step 1: Setup OpenWRT SDK**  
1. Download and install the **OpenWRT SDK** for your target platform:  
   ```bash
   git clone https://git.openwrt.org/openwrt/openwrt.git
   cd openwrt
   ./scripts/feeds update -a
   ./scripts/feeds install -a
   ```

### **Step 2: Add the EasyMesh App to OpenWRT Package Sources**  
```bash
cd package
git clone https://github.com/aumt/luci-app-easymesh.git
```

### **Step 3: Compile the Package**  
1. Go back to OpenWRT’s root directory:  
   ```bash
   cd ../
   ```
2. Select the package using `make menuconfig`:  
   ```bash
   make menuconfig
   ```
   - Navigate to `LuCI` → `Applications` → `luci-app-easymesh`  
   - Select `<M>` to compile it as a module  

3. Compile the package:  
   ```bash
   make package/luci-app-easymesh/compile V=s
   ```
4. Once compiled, the packages land in `bin/packages/<arch>/base/`. Which **format** you get is decided by the SDK you chose in Step 1, not by this repository:

   | SDK | Package manager | Output |
   |---|---|---|
   | OpenWrt **25.12** and newer | `apk` | `.apk` |
   | OpenWrt **24.10** and older | `opkg` | `.ipk` |

   The two formats also use different file-name rules, so don't copy a name from one section to the other:

   | SDK | `luci-app-easymesh` | `luci-i18n-easymesh-zh-cn` |
   |---|---|---|
   | 25.12 → `.apk` | `luci-app-easymesh-3.8.17-r1.apk` | `luci-i18n-easymesh-zh-cn-0.261001.20149.apk` |
   | 24.10 → `.ipk` | `luci-app-easymesh_3.8.17-r1_all.ipk` | `luci-i18n-easymesh-zh-cn_0.261001.20149_all.ipk` |

   - **apk** uses hyphens and carries **no architecture field in the name**.
   - **ipk** uses underscores and ends in `_all`.
   - The translation package's version (`0.261001.20149`) is derived from the build date, so it changes on every build — match it with a wildcard, not a literal name.

   Building `luci-app-easymesh` also builds `luci-i18n-easymesh-zh-cn` (Simplified Chinese). That package is **hidden** in `menuconfig` — it is pulled in automatically when Simplified Chinese is enabled (`LuCI` → `Translations` → `zh_Hans`), or you can force it by adding `CONFIG_PACKAGE_luci-i18n-easymesh-zh-cn=m` to `.config`.  

   > Both packages are `PKGARCH:=all` (apk: `arch: noarch`) — they contain only Lua, shell and compiled `.lmo` files, so a package built with an **x86-64 SDK installs fine on an arm64/aarch64 router**. You do not need a matching-architecture SDK.

# **📥 Installing `luci-app-easymesh`**

First check which package manager your firmware uses:

```sh
apk --version    # OpenWrt 25.12 and newer
opkg --version   # OpenWrt 24.10 and older
```

Then download the matching file from [Releases](https://github.com/aumt/luci-app-easymesh/releases).

## **OpenWrt 25.12 and newer — `.apk`**

### **Option 1: Install via LuCI UI**
1. Download `luci-app-easymesh-*.apk` — and `luci-i18n-easymesh-zh-cn-*.apk` too if you want a Simplified Chinese interface.
2. Navigate to **System → Software** in LuCI.
3. Click **Upload Package**, select the `.apk` file, and install it.

### **Option 2: Install via CLI (SSH/Terminal)**
```sh
apk update
apk add --allow-untrusted /path/to/luci-app-easymesh-*.apk
apk add --allow-untrusted /path/to/luci-i18n-easymesh-zh-cn-*.apk
```

> The release packages are not signed with your firmware's key, hence `--allow-untrusted`.

## **OpenWrt 24.10 and older — `.ipk`**

### **Option 1: Install via LuCI UI**
1. Download `luci-app-easymesh_*.ipk` — and `luci-i18n-easymesh-zh-cn_*.ipk` too if you want a Simplified Chinese interface.
2. Navigate to **System → Software** in LuCI.
3. Click **Upload Package**, select the `.ipk` file, and install it.

### **Option 2: Install via CLI (SSH/Terminal)**
```sh
opkg update
opkg install /path/to/luci-app-easymesh_*.ipk
opkg install /path/to/luci-i18n-easymesh-zh-cn_*.ipk
```

---

# **🤖 Prebuilt Packages (GitHub Actions)**

You don't have to build anything yourself. Every push, every `v*` tag and every pull request triggers [`.github/workflows/build.yml`](.github/workflows/build.yml), which builds this package with **both** SDKs at once and uploads four files:

| Artifact | SDK | Files inside |
|---|---|---|
| `openwrt-25.12-apk` | OpenWrt 25.12.5 SDK | `luci-app-easymesh-*.apk`, `luci-i18n-easymesh-zh-cn-*.apk` |
| `openwrt-24.10-ipk` | OpenWrt 24.10.8 SDK | `luci-app-easymesh_*.ipk`, `luci-i18n-easymesh-zh-cn_*.ipk` |

Collect them from the **Actions** tab (as a run artifact), or from **Releases**. A push to `main` publishes a release automatically, tagged `easymesh-build-<YYMMDDHHMMSS>`; pushing a `v*` tag, or running the workflow by hand with `release_tag` filled in, publishes one under that name instead. Leaving `release_tag` empty on a manual run produces artifacts only — no release. Then install the pair that matches your firmware's package manager, as described above.

To start a build by hand: **Actions → Build luci-app-easymesh → Run workflow**.

> The workflow compiles **only this package plus the host tools it needs** (`po2lmo` for the translation), not the runtime dependency tree — `mac80211`, `hostapd`, `batman-adv`, `batctl`, `dawn`, `iwinfo` and `linux-firmware` are *not* rebuilt. They are dependencies to be *installed*, not sources to be compiled, and skipping them doesn't change the packages' `depends` metadata at all. This is what keeps a run at a couple of minutes instead of pulling a 582 MB firmware blob.

---

# **⚠️ Required Kernel & Wireless Packages**

`luci-app-easymesh` drives **batman-adv** and **802.11s mesh**, which are *not* part of a default OpenWrt build. The package declares them as dependencies, so a normal install pulls them in — but they must be available in your configured package feeds, and on a **self-built firmware** those kernel modules have to have been built into it in the first place.

| Package | Needed for |
|---|---|
| `kmod-batman-adv` | the batman-adv kernel module — no module, no `bat0` |
| `batctl-default` | the `batctl` CLI behind the Mesh Status table |
| `kmod-cfg80211` | cfg80211 wireless stack used by the mesh radios |
| `dawn` | 802.11k/v/r roaming daemon |
| `wpad-mesh-openssl` (or `-mbedtls` / `-wolfssl`) | **802.11s mesh support. The default `wpad-basic-*` does NOT have it** — mesh interfaces silently fail to come up |
| `luci-proto-batman-adv` | the `batadv` protocol handler in LuCI |
| `luci-compat` + `luci-lua-runtime` | this is a Lua CBI app; these provide the Lua runtime layer |
| `libiwinfo-lua` | Lua `iwinfo` bindings, used to label the radio list |
| `bash` | `root/easymesh/easymesh.sh` is a bash script |

> A `wpad-mesh-*` package **replaces** whichever `wpad-*` is installed (they all `PROVIDES: wpad`). Switch deliberately, and pick the TLS backend the rest of your firmware already uses.

---

# **🛠️ How to Setup a Basic Mesh Network (1 Server + 2 Nodes)**  

### **Step 1: Setup the Mesh Server**
1. **Disable/Delete any active wireless networks** in OpenWRT (Go to `Network → Wireless`).  
2. **Go to `Network → EasyMesh`**  
3. Select **"Server"** for Mesh Mode.
   ![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/blob/main/images/1740359288453.png)
5. **Enter your WiFi SSID** (This is the main WiFi network all devices will connect to).  
6. **Select the WiFi Radio** for the **regular AP**. *(Recommended: Use a different radio than the mesh backhaul for best performance.)*  
7. **Select the Mesh Radio** and enter a separate SSID. *(The app will automatically append `-mesh` to your mesh SSID.)*
   ![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/raw/main/images/1740359253028.png)
9. **Enable Password Protection**, enter a Mesh Password, and click **Save & Apply**.  
10. Click **"Reapply EasyMesh Settings"** to deploy the APs and activate mesh networking.  

🔹 **Verify Setup:**  
- **Go to `Network → Wireless`** to check that the WiFi networks were added.
  ![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/blob/main/images/1740359342226.png)
- **Go to `Network → Interfaces`** to confirm that the Batman (`bat0`) device and (`mesh_batman`) interface was added.
  ![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/blob/main/images/1740359385796.png)

---

### **Step 2: Setup a Mesh Node**
1. **Go to `Network → EasyMesh` on the second router.**  
2. **Select "Client" for Mesh Mode.**
   ![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/blob/main/images/1740359451089.png)
4. **Enter the same WiFi SSID, Mesh SSID, and Password** as the server.  
5. **Ensure you select the same WiFi radio type** (AX, AC, b/g/n) for both WiFi SSID and Mesh SSID.  
6. Click **Save & Apply**, then click **"Reapply EasyMesh Settings"**.  
7. **Go to `AP Mode` tab** and select a **hostname** (e.g., `node2`, `node3`, etc.).  
8. **Set to DHCP (recommended for Dumb AP nodes)** or configure a **Static IP** in the same range as your Mesh Server.
   ![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/blob/main/images/7.png)
10. Click **Save & Apply**, then click **"Enable Dumb AP Mode"**.  

---

### **Step 3: Repeat for Additional Mesh Nodes**
- **Use the same WiFi SSID, Mesh SSID, and Password** for every node.  
- **Ensure all nodes use the same WiFi radio type (AX, AC, b/g/n).**  

---

### **Step 4: Verify Neighbor Nodes**
1. **Go to `Network → EasyMesh` on the Mesh Server**  
   - **Check that nearby nodes are listed under Mesh Status.**
     ![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/blob/main/images/1740359534195.png)
2. **Go to `Network → Wireless`**  
   - **Verify that Mesh Backhaul Networks are communicating with the server.**
     ![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/blob/main/images/1740359602760.png)
3. **Find your Mesh Nodes' IPs in `DHCP Devices` under `Status → Overview`.**
   ![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/blob/main/images/1740359643565.png) 
5. **Access a node by entering its IP in a browser.**  

---

### **Step 5: (Optional) Activate TorGuard WireGuard VPN on the Mesh Server**
![EasyMesh Screenshot](https://github.com/torguardvpn/luci-app-easymesh/blob/main/images/1740359720850.png)
1. **Go to `Network → TorGuard WireGuard`.**  
2. **Enter your WireGuard Username & Password.**  
3. **Select your preferred WireGuard server location.**  
4. **Enable WireGuard and click Save & Apply.**  
5. **Click "Start WireGuard"** to tunnel all mesh network traffic through the VPN.  

---

# **❓ FAQ (Common Questions & Issues)**  

### **Do I have to use WireGuard with this app?**  
**No.** You can deploy a standard Mesh WiFi network on an OpenWRT router **without a VPN** in minutes.  

### **Can I run both the main WiFi AP and Mesh AP on the same radio?**  
You can, **but it’s not recommended**.  
For best performance, use **separate radios** for each network.  
- **If running both on the same radio:**  
  - **Limitations:** Limited channels reduce performance.  
  - **Disable Batman Advanced features:** Disable **bonding** and **fragmentation** to reduce overhead.  

### **Can I add wired devices or a router that doesn’t support mesh?**  
Yes. If using a **wired OpenWRT router (x86 device) without mesh support**:  
- **Go to `Network → Interfaces` and manually select `bat0` as the device on the `mesh_batman` interface.**  

### **How do I recover a node after enabling Dumb AP mode?**  
- If you can't access it via Wifi connect it to your server **via LAN cable**, then find the node IP under DHCP and connect in a web browser.  

### **Best way to change Mesh WiFi settings?**  
1. **Change settings on each node first.**  
2. **Update settings on the Mesh Server last.**  
3. **Reapply settings** to reconnect all nodes.  

---

🔥 **Now your OpenWRT Mesh WiFi is fully set up! 🚀**  
