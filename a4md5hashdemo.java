import java.security.MessageDigest;
import java.util.Scanner;

public class a4md5hashdemo {
    public static void main(String[] args) {
        try {
  
            Scanner sc = new Scanner(System.in);
            System.out.print("Enter text to hash using MD5: ");
            String input = sc.nextLine();


            MessageDigest md = MessageDigest.getInstance("MD5");

            md.update(input.getBytes());

            byte[] digestBytes = md.digest();

            StringBuilder sb = new StringBuilder();
            for (byte b : digestBytes) {
                sb.append(String.format("%02x", b));
            }

            System.out.println("MD5 Hash: " + sb.toString());
            sc.close();
        } catch (Exception e) {
            System.out.println("Error: " + e);
        }
    }
}