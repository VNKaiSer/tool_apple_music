import winreg as reg

def set_proxy(proxy_address):
    """Bật proxy với địa chỉ đã cho."""
    try:
        # Đường dẫn đến registry cho cài đặt proxy
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        
        # Mở registry
        registry = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_path, 0, reg.KEY_SET_VALUE)
        
        # Thiết lập proxy
        reg.SetValueEx(registry, "ProxyEnable", 0, reg.REG_DWORD, 1)  # Bật proxy
        reg.SetValueEx(registry, "ProxyServer", 0, reg.REG_SZ, proxy_address)  # Địa chỉ proxy
        
        # Đóng registry
        reg.CloseKey(registry)
        print(f"Proxy đã được thiết lập: {proxy_address}")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi thiết lập proxy: {e}")

def unset_proxy():
    """Tắt proxy."""
    try:
        # Đường dẫn đến registry cho cài đặt proxy
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        
        # Mở registry
        registry = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_path, 0, reg.KEY_SET_VALUE)
        
        # Tắt proxy
        reg.SetValueEx(registry, "ProxyEnable", 0, reg.REG_DWORD, 0)  # Tắt proxy
        reg.DeleteValue(registry, "ProxyServer")  # Xóa địa chỉ proxy
        
        # Đóng registry
        reg.CloseKey(registry)
        print("Proxy đã được tắt.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi tắt proxy: {e}")

def get_proxy():
    """Lấy địa chỉ proxy hiện tại."""
    try:
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        registry = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_path)
        
        proxy_enable = reg.QueryValueEx(registry, "ProxyEnable")[0]
        proxy_server = reg.QueryValueEx(registry, "ProxyServer")[0] if proxy_enable else None
        
        reg.CloseKey(registry)
        
        if proxy_enable:
            return proxy_server  # Trả về địa chỉ proxy
        else:
            return None  # Không bật proxy
    except Exception as e:
        print(f"Đã xảy ra lỗi khi lấy địa chỉ proxy: {e}")
        return None

# Sử dụng hàm
# Địa chỉ proxy cần thiết lập (không có http://)
proxy = "hades.p.shifter.io:19787"  # Proxy address without 'http://'
set_proxy(proxy)

# Lấy địa chỉ proxy hiện tại
current_proxy = get_proxy()
if current_proxy:
    print(f"Proxy hiện tại: {current_proxy}")
else:
    print("Proxy hiện tại không được bật.")

# Để tắt proxy
# unset_proxy()
