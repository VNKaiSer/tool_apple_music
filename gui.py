import sys
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

sys.path.append('./utils')
sys.path.append('./')
import main
from utils import import_id 
from utils import import_card


def add_id():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                import_id.process_data(content)
                messagebox.showinfo("Thành công", "Thêm id thành công")
        
         
        
    except Exception as e:
        print(e)
        messagebox.showerror("Thất bại", "Error: Thêm thất bại vui lòng kiểm tra định dạng file hoặc network" )
def add_card():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                import_card.process_data(content)
                messagebox.showinfo("Thành công", "Thêm thẻ thành công")
        
    except Exception as e:
        print(e)
        messagebox.showerror("Thất bại", "Error: Thêm thất bại vui lòng kiểm tra định dạng file hoặc network" )
def run_app():
    main.run()
    

root = Tk()
root.title("Tool apple music")
root.withdraw()  # Ẩn cửa sổ chính ban đầu

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Đặt cửa sổ vào giữa màn hình
app_width = 400
app_height = 300
x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
root.geometry(f"{app_width}x{app_height}+{x}+{y}")

# Hiển thị cửa sổ chính
root.deiconify()

menu = Menu(root)
root.config(menu=menu)
add_data_menu = Menu(menu)
menu.add_cascade(label='Thêm dữ liệu', menu=add_data_menu)
add_data_menu.add_command(label='Thêm id', command=add_id)
add_data_menu.add_command(label='Thêm thẻ', command=add_card)
add_data_menu.add_separator()

featuremenu = Menu(menu)
menu.add_cascade(label='Chức năng', menu=featuremenu)
featuremenu.add_command(label='Chạy tool', command=run_app)
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About')

exit_menu = Menu(menu)
menu.add_cascade(label='Exit', menu=exit_menu)
exit_menu.add_command(label='Exit', command=root.quit)

mainloop()
