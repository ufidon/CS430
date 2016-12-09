using System;
using System.IO;
using System.Diagnostics;

class StandardOutputExample
{
	public static void Main(string[] args)
	{
		Console.WriteLine( "Number of arguments:" + args.Length + " arguments.");
		Console.WriteLine ("Argument List:");
		foreach(string arg in args)
		{
			Console.WriteLine (arg);
		}

		/*
		#      0     1  2                          3  4    5   6          7    8	
		# AesU -e[d] -k key <-i initial_vector>    -m ecb  -in input_file -out output_file
		*/
		Console.WriteLine ("acess parameters one by one");

		for (int i=0; i<args.Length; ++i)
		{
			Console.WriteLine (args [i]);
		}

		/* openssl>
		# aes-128-ecb -d -K 11223344556677889900112233445566
		# -v -nosalt -in poem128ecb.txt -out dpoem128ecb.txt
		*/

		int keylen = args [2].Length;
		string cipher = "-aes-" + (keylen * 4).ToString () + "-" + args [4];


		Process process = new Process();
		process.StartInfo.FileName = "openssl";
		process.StartInfo.Arguments = " enc " + cipher + " -K " + args[2] + " -v -nosalt " + " " +
			args[5] + " " + args[6] + " " + args[7] + " " + args[8];
		
		process.StartInfo.UseShellExecute = false;
		process.StartInfo.RedirectStandardOutput = true;        
		process.Start();

		// Synchronously read the standard output of the spawned process. 
		StreamReader reader = process.StandardOutput;
		string output = reader.ReadToEnd();

		// Write the redirected output to this application's window.
		Console.WriteLine(output);

		process.WaitForExit();
		process.Close();

		Console.WriteLine("\n\nPress any key to exit.");
		Console.ReadLine();
	}
}