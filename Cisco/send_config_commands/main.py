from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import SSHException
from getpass import getpass
import yaml

# Get username and password from user
print("Enter username and password that you wish to run the script with")
username = input("Username: ")
password = getpass()

# Read the file devices_list.yml
with open('devices_list.yml', 'r') as infile:
    try:
        devices_list = yaml.load(infile, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        print(exc)

# Read the file command_list.yml
with open('config_commands_list.yml', 'r') as infile:
    try:
        commands_list = yaml.load(infile, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        print(exc)

# Set the variable proceed to true for the user dialogue
proceed = True

# Print what devices and what commands will be run
print("The following devices:")
for device in devices_list:
    print(device)
print("will be configured with the following commands:")
for command in commands_list:
    print(command)

# Ask the user for input in order to proceed or exit
response = input("Do you want to proceed? (Y/N): ")

# Check if the user responded N or Y
while proceed:
    if response.upper() == "Y":
        # Write a bunch of ### to make the output more readable
        print("##################################################")
        # Run through the list of devices from the file devices_list.yml and send the pre-defined commands
        for device_ip in devices_list:
            try:
                # Connect to the device
                net_connect = ConnectHandler(device_type='cisco_ios', ip=device_ip, username=username,
                                             password=password)
                # Print out successful connection
                print(f"Connected to device: {device_ip}")
                # Send the list of commands
                output = net_connect.send_config_set(commands_list)
#                for command in commands_list:
#                  print(f"Sending command {command}")
#                    output = net_connect.send_config_set(command)
#                    print(output)
                # Save the configuration
                print("Saving configuration")
                net_connect.save_config()
                # Close the ssh session
                net_connect.disconnect()
                print(f"Disconnected from device: {device_ip}")
                # Print a bunch of ### to separate each run and make it more readable
                print("##################################################")
            # Error handling
            except NetMikoAuthenticationException:
                with open("results/authentication_timeout.txt", 'a') as file:
                    file.write(f'Auth timeout to device: {device_ip}\n')
                print(f'Auth timeout to device: {device_ip}')
                # Print a bunch of ### to separate each run and make it more readable
                print("##################################################")
            except NetMikoTimeoutException:
                with open("results/device_timeout.txt", 'a') as file:
                    file.write(f'Timeout to device: {device_ip}\n')
                print(f'Timeout to device: {device_ip}')
                # Print a bunch of ### to separate each run and make it more readable
                print("##################################################")
            except SSHException:
                with open("results/ssh_issue.txt", 'a') as file:
                    file.write(f'SSH issue to device: {device_ip}\n')
                print(f'SSH issue to device: {device_ip}')
                # Print a bunch of ### to separate each run and make it more readable
                print("##################################################")
        # Change the variable "proceed" to False in order to prevent an infinite loop
        proceed = False
    elif response.upper() == "N":
        # Change the variable proceed to False in order to stop the loop
        proceed = False
    else:
        # If the user responds with anything other than Y or N, ask the user again to respond with Y or N
        print("Please answer Y or N")
        response = input("Do you want to proceed? (Y/N)")

# Print some crap to show that the program has ended
print("**************************************************")
print("**************************************************")
print("**************************************************")
print("***************** End of program *****************")
print("**************************************************")
print("**************************************************")
print("**************************************************")
