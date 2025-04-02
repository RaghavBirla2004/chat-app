import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

class ChatClient:
    def _init_(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("500x600")
        
        # Network setup
        self.client_socket = None
        self.running = False
        
        # GUI elements
        self.setup_gui()
        
    def setup_gui(self):
        # Connection frame
        conn_frame = Frame(self.root)
        conn_frame.pack(pady=10)
        
        Label(conn_frame, text="Server IP:").grid(row=0, column=0, padx=5)
        self.server_ip = Entry(conn_frame, width=15)
        self.server_ip.grid(row=0, column=1, padx=5)
        self.server_ip.insert(0, ": 10.25.203.254")  # Default starting IP
        
        Label(conn_frame, text="Port:").grid(row=1, column=0, padx=5)
        self.port_entry = Entry(conn_frame, width=15)
        self.port_entry.grid(row=1, column=1, padx=5)
        self.port_entry.insert(0, "55555")
        
        # Connect/Disconnect buttons
        button_frame = Frame(self.root)
        button_frame.pack(pady=5)
        
        self.connect_button = Button(button_frame, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(side=LEFT, padx=5)
        
        self.disconnect_button = Button(button_frame, text="Disconnect", command=self.disconnect, state=DISABLED)
        self.disconnect_button.pack(side=LEFT, padx=5)
        
        # Status frame
        status_frame = Frame(self.root)
        status_frame.pack(pady=5)
        
        self.status_label = Label(status_frame, text="Status: Disconnected", fg="red")
        self.status_label.pack()
        
        # Chat display
        self.chat_display = ScrolledText(self.root, height=15, width=50, state=DISABLED)
        self.chat_display.tag_config('received', foreground='blue')
        self.chat_display.pack(pady=10)
        
        # Message entry
        msg_frame = Frame(self.root)
        msg_frame.pack(pady=10)
        
        self.msg_entry = Entry(msg_frame, width=40)
        self.msg_entry.pack(side=LEFT, padx=5)
        self.msg_entry.bind("<Return>", self.send_message)
        
        self.send_button = Button(msg_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=LEFT, padx=5)
        self.send_button.config(state=DISABLED)
    
    def connect_to_server(self):
        server_ip = self.server_ip.get()
        port = self.port_entry.get()
        
        if not server_ip or not port:
            messagebox.showerror("Error", "Please enter server IP and port")
            return
        
        try:
            port = int(port)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, port))
            
            self.running = True
            self.status_label.config(text=f"Status: Connected to {server_ip}", fg="green")
            self.connect_button.config(state=DISABLED)
            self.disconnect_button.config(state=NORMAL)
            self.send_button.config(state=NORMAL)
            
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            self.update_chat(f"Connected to server {server_ip}:{port}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")
    
    def disconnect(self):
        self.running = False
        try:
            if self.client_socket:
                self.client_socket.close()
        except:
            pass
        
        self.status_label.config(text="Status: Disconnected", fg="red")
        self.connect_button.config(state=NORMAL)
        self.disconnect_button.config(state=DISABLED)
        self.send_button.config(state=DISABLED)
        self.update_chat("Disconnected from server.\n")
    
    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.update_chat(f"Server: {message}\n", 'received')
            except:
                self.update_chat("Disconnected from server.\n")
                self.status_label.config(text="Status: Disconnected", fg="red")
                self.connect_button.config(state=NORMAL)
                self.disconnect_button.config(state=DISABLED)
                self.send_button.config(state=DISABLED)
                break
    
    def send_message(self, event=None):
        message = self.msg_entry.get()
        if message and self.client_socket:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.update_chat(f"You: {message}\n")
                self.msg_entry.delete(0, END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {e}")
    
    def update_chat(self, message, tag=None):
        self.chat_display.config(state=NORMAL)
        if tag:
            self.chat_display.insert(END, message, tag)
        else:
            self.chat_display.insert(END, message)
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)
    
    def on_closing(self):
        self.disconnect()
        self.root.destroy()

if _name_ == "_main_":
    root = Tk()
    app = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()