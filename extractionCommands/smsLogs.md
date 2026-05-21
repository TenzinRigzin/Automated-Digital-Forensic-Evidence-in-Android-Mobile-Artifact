# 📱 Mobile SMS Data Extraction Guide (via ADB)

This guide walks you through the step-by-step process of using **Android Debug Bridge (ADB)** to securely extract text message history directly from an Android device onto your computer without relying on cloud backups.

---

## 🛠️ Step 1: Prepare Your Mobile Device
Before running terminal commands, your phone must be configured to allow direct computer communication.

1. On your Android phone, navigate to **Settings** > **About Phone**.
2. Locate the **Build Number** field and tap it **7 times** continuously. A popup will read: *"You are now a developer!"*
3. Return to the main Settings menu, locate the newly unlocked **Developer Options**, and switch **USB Debugging** to **ON**.
4. Connect your phone to your computer using a high-quality USB data cable.

---

## 🔌 Step 2: Establish and Authorize the Connection
Open your computer terminal and verify that your system can see the hardware.

1. Type the following pairing command:
   ```cmd
   adb devices
   ```
2. **Look at your phone screen immediately!** A security prompt will appear reading: *"Allow USB debugging?"*
3. Check the box for **"Always allow from this computer"** and tap **Allow** or **OK**.
4. Run the device command a second time to verify authorization:
   ```cmd
   adb devices
   ```
* **Success Look:** `ZY22G8H9B2    device`  
* **Error Look:** `ZY22G8H9B2    unauthorized` *(If unauthorized, unplug the USB cable, plug it back in, and accept the phone popup).*

---

## 💾 Step 3: Extract SMS Data Without Root
Android strictly locks raw database files like `mmssms.db` for user privacy. To bypass this restriction on non-rooted phones, you can query Android’s internal **Content Provider** directly to stream the texts into a clean file.

Run this exact command in your terminal to query and dump the message database:

```cmd
adb shell "content query --uri content://sms/ --projection thread_id:address:date:body" > %USERPROFILE%\Desktop\data_input\sms_backup.txt
```

### What this command does:
* **`content query --uri content://sms/`**: Securely requests Android's internal messaging registry to output text logs.
* **`--projection thread_id:address:date:body`**: Filters out thousands of lines of hidden tracking metrics, isolating only the data needed for analysis: conversation group ID, sender phone number, epoch timestamp, and the actual message text.
* **`> ...\sms_backup.txt`**: Pipes that live stream across the USB cord and packages it directly as a clean text file inside your local AI `data_input` directory.

---

## 🛑 Troubleshooting Permission Barriers

### Issue: `adb.exe: device unauthorized` or `ADB_VENDOR_KEYS` error
This means the phone's cryptographic handshake was missed or rejected.
1. Force-kill the stuck terminal connection server:
   ```cmd
   adb kill-server
   ```
2. Kickstart it fresh:
   ```cmd
   adb start-server
   ```
3. Pull down your phone's notification bar, change the USB option from *"Charging only"* to **"File Transfer / MTP"**, and accept the security popup.

### Issue: Empty file or zero rows extracted
Some modern Android overlays (like Samsung OneUI or Xiaomi MIUI) require an extra security toggle to let ADB read messages.
1. Go back into your phone's **Developer Options**.
2. Look for a setting named **"USB Debugging (Security settings)"** or **"Allow granting permissions via ADB"**.
3. Turn it **ON** and re-run the extraction command.
