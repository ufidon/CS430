import java.io.*;


public class aesu {

    public static void main(String args[]) {

        String s = null;

        try {
        	
        	
        	System.out.println("Number of arguments:" + args.length + " arguments.");
        	System.out.println ("Argument List:");
        	for(int i=0; i<args.length; ++i) {
        	    System.out.println(args[i]);
        	}
        	
    		/*
    		#      0     1  2                          3  4    5   6          7    8	
    		# AesU -e[d] -k key <-i initial_vector>    -m ecb  -in input_file -out output_file
    		*/

    		/* openssl>
    		# aes-128-ecb -d -K 11223344556677889900112233445566
    		# -v -nosalt -in poem128ecb.txt -out dpoem128ecb.txt
    		*/

    		int keylen = args [2].length();
    		String cipher = "-aes-" + Integer.toString(keylen * 4) + "-" + args [4];
        	
            
        	// run openssl command
    		String opensslcmd = String.format("openssl enc %s -K %s -v -nosalt -in %s -out %s", args[0], args[2], args[6], args[8]);

            // using the Runtime exec method:
            Process p = Runtime.getRuntime().exec(opensslcmd);
            
            BufferedReader stdInput = new BufferedReader(new 
                 InputStreamReader(p.getInputStream()));

            BufferedReader stdError = new BufferedReader(new 
                 InputStreamReader(p.getErrorStream()));

            // read the output from the command
            System.out.println("Here is the standard output of the command:\n");
            while ((s = stdInput.readLine()) != null) {
                System.out.println(s);
            }
            
            // read any errors from the attempted command
            System.out.println("Here is the standard error of the command (if any):\n");
            while ((s = stdError.readLine()) != null) {
                System.out.println(s);
            }
            
            System.exit(0);
        }
        catch (IOException e) {
            System.out.println("exception happened - here's what I know: ");
            e.printStackTrace();
            System.exit(-1);
        }
    }
}