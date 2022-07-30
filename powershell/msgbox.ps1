Add-Type -AssemblyName System.Windows.Forms;
[System.Windows.Forms.MessageBox]::Show($args[0], $args[1], 'OK', [System.Windows.Forms.MessageBoxIcon]::Information);