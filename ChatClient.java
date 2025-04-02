import java.io.*;
import java.net.*;
import java.util.Scanner;

public class ChatClient {
    private static final String SERVER_IP = "192.168.50.123"; 
    private static final int SERVER_PORT = 9311;

    public static void main(String[] args) {
        try (Socket socket = new Socket(SERVER_IP, SERVER_PORT)) {
            System.out.println("Connected to chat server at " + SERVER_IP);

            // Thread to read messages from server
            new Thread(new ServerListener(socket)).start();

            // Read input from user and send to server
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            Scanner scanner = new Scanner(System.in);

            while (true) {
                String message = scanner.nextLine();
                out.println(message);
            }
        } catch (IOException e) {
            System.out.println("Server connection error: " + e.getMessage());
        }
    }

    // Listens for incoming messages from the server
    private static class ServerListener implements Runnable {
        private Socket socket;
        private BufferedReader in;

        public ServerListener(Socket socket) {
            this.socket = socket;
        }

        @Override
        public void run() {
            try {
                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                String serverMessage;
                while ((serverMessage = in.readLine()) != null) {
                    System.out.println(serverMessage);
                }
            } catch (IOException e) {
                System.out.println("Disconnected from server");
            }
        }
    }
}