import org.apache.commons.cli.*;
import java.util.*;
import java.io.*;
import java.nio.file.*;


public class aesu {
	
	public static  byte[] readBinaryFile(String aFileName) throws IOException {
		    Path path = Paths.get(aFileName);
		    return Files.readAllBytes(path);
		  }
		  
	public static  void writeBinaryFile(byte[] aBytes, String aFileName) throws IOException {
		    Path path = Paths.get(aFileName);
		    Files.write(path, aBytes); //creates, overwrites
		  }	

	public static void main(String[] args) {
		
		
		
		//  AesU -e[d] -k key <-i initial_vector>    -m CBC  -in input_file -out output_file
		System.out.println("Welcome to my aesu!");
		
		String key, initvec, mode, infile, outfile;
		
		// create Options object
		Options options = new Options();

		// add encryption option
		options.addOption("e", false, "encryption");
		// add decryption option
		options.addOption("d", false, "decryption");
		// add Key option
		options.addOption("K", true, "key");
		// add initial vector
		options.addOption("i", true, "initial vector");
		// add cipher operational mode
		options.addOption("m", true, "operational mode");
		// add input file
		options.addOption("in", true, "input file");
		// add output file
		options.addOption("out", true, "output file");
		
		
		
		CommandLineParser parser = new DefaultParser();
		
		try{
			CommandLine cmd = parser.parse( options, args);
			
			if(cmd.hasOption("e")) {
				System.out.println("encrytion");	
			}
			
			if(cmd.hasOption("d")) {
				System.out.println("decrytion");
			}
			
			key = cmd.getOptionValue("K");
			if(key != null) {
				System.out.println("key:"+key);
			}
			
			initvec = cmd.getOptionValue("i");
			if(initvec != null) {
				System.out.println("initial vector:"+initvec);
			}
			
			mode = cmd.getOptionValue("m");
			if(mode != null) {
				System.out.println("operational mode:"+mode);
			}
			
			infile = cmd.getOptionValue("in");
			if(infile != null) {
				System.out.println("input file:"+infile);
			}

			outfile = cmd.getOptionValue("out");
			if(outfile != null) {
				System.out.println("output file:"+outfile);
			}

		}
		catch(org.apache.commons.cli.UnrecognizedOptionException e)
		{
			System.out.println(e.toString());
			infile = "input.txt";
			outfile = "output.txt";
		}
		catch(Throwable any)
		{
			System.out.println(any.toString());
			infile = "input.txt";
			outfile = "output.txt";
		}
		
		
		// test file read and write
	
		byte[] randdata = new byte[1024];
		for(int i=0; i<1024; ++i)
		{
			randdata[i] = 0x5a;
		}
		
		try{

			writeBinaryFile(randdata, outfile);
			randdata = readBinaryFile(outfile);
			
			for(int i=0; i<1024; ++i)
			{
				System.out.println(randdata[i]);
			}
			
		}
		catch(Throwable all)
		{
			System.out.println(all.toString());
		}
		
	}

}
