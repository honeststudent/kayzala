
import java.security.*;

public class a6digitalsignaturedemo {
    public static void main(String[] args) {
        try {
            // Step 1: Generate key pair (public + private keys)
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("DSA");
            keyGen.initialize(2048); // key size
            KeyPair pair = keyGen.generateKeyPair();
            PrivateKey privateKey = pair.getPrivate();
            PublicKey publicKey = pair.getPublic();

            // Step 2: Create a Signature object and initialize it with the private key
            Signature sign = Signature.getInstance("SHA256withDSA");
            sign.initSign(privateKey);

            // Step 3: Input message
            String message = "This is a digital signature demo by Aditya Kale";
            byte[] messageBytes = message.getBytes();

            // Step 4: Supply the message to be signed
            sign.update(messageBytes);

            // Step 5: Generate the digital signature (signing)
            byte[] digitalSignature = sign.sign();

            // Step 6: Display signature in hexadecimal form
            System.out.println("Original Message: " + message);
            System.out.println("\nDigital Signature (Hex):");
            StringBuilder sb = new StringBuilder();
            for (byte b : digitalSignature) {
                sb.append(String.format("%02x", b));
            }
            System.out.println(sb.toString());

            // Step 7: Verify the signature using the public key
            Signature verifySign = Signature.getInstance("SHA256withDSA");
            verifySign.initVerify(publicKey);
            verifySign.update(messageBytes);

            boolean isVerified = verifySign.verify(digitalSignature);

            // Step 8: Display verification result
            System.out.println("\nSignature Verified: " + isVerified);

        } catch (Exception e) {
            System.out.println("Error: " + e);
        }
    }
}
