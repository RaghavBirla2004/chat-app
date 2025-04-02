import java.io.*;
import java.net.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ChatClient {
    private static final String SERVER_IP = "192.168.50.123"; // Change to the server's IP
    private static final int SERVER_PORT = 12345;
    
    private JFrame frame = new JFrame("Chat Client");
    private JTextField textField = new JTextField(30); // Reduced width to make space for button
    private JTextArea messageArea = new JTextArea(15, 40);
    private JButton sendButton = new JButton("Send");
    private PrintWriter out;
    
    public ChatClient() {
        // GUI Setup
        textField.setEditable(false);
        messageArea.setEditable(false);
        frame.getContentPane().setLayout(new BorderLayout());
        
        // Create panel for input area (text field + button)
        JPanel inputPanel = new JPanel();
        inputPanel.setLayout(new BorderLayout());
        inputPanel.add(textField, BorderLayout.CENTER);
        inputPanel.add(sendButton, BorderLayout.EAST);
        
        frame.getContentPane().add(new JScrollPane(messageArea), BorderLayout.CENTER);
        frame.getContentPane().add(inputPanel, BorderLayout.SOUTH);
        frame.pack();
        
        // Add Listeners
        ActionListener sendAction = new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                sendMessage();
            }
        };
        
        textField.addActionListener(sendAction); // Send on Enter key
        sendButton.addActionListener(sendAction); // Send on button click
    }
    
    private void sendMessage() {
        if (!textField.getText().trim().isEmpty()) {
            out.println(textField.getText());
            textField.setText("");
        }
        textField.requestFocus(); // Return focus to text field
    }
    
    private String getName() {
        return JOptionPane.showInputDialog(
            frame,
            "Choose a screen name:",
            "Screen name selection",
            JOptionPane.PLAIN_MESSAGE
        );
    }
    
    private void run() throws IOException {
        try {
            Socket socket = new Socket(SERVER_IP, SERVER_PORT);
            out = new PrintWriter(socket.getOutputStream(), true);
            
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            
            String name = getName();
            out.println(name); // Send the name first
            
            frame.setTitle("Chat Client - " + name);
            textField.setEditable(true);
            
            // Thread to read messages from server
            new Thread(new Runnable() {
                public void run() {
                    String message;
                    try {
                        while ((message = in.readLine()) != null) {
                            messageArea.append(message + "\n");
                        }
                    } catch (IOException e) {
                        System.err.println("Error reading from server: " + e.getMessage());
                    }
                }
            }).start();
            
        } catch (UnknownHostException e) {
            System.err.println("Don't know about host " + SERVER_IP);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't get I/O for the connection to " + SERVER_IP);
            System.exit(1);
        }
    }
    
    public static void main(String[] args) throws IOException {
        ChatClient client = new ChatClient();
        client.frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        client.frame.setVisible(true);
        client.run();
    }
}