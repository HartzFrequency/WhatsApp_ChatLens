import os

def format_whatsapp_chat(input_folder='Input_dataWOMedia', output_folder='Output'):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"formatted_{filename}")
            
            with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
                previous_date = None
                previous_sender = None
                
                for line in infile:
                    try:
                        # Split the line by the first hyphen to separate the date and time part
                        date_time_part, message_part = line.split(' - ', 1)
                        # Parse the date and time part
                        date_str, time_str = date_time_part.split(', ')
                        
                        # Check if the date has changed
                        if date_str != previous_date:
                            if previous_date is not None:
                                # Write two blank lines when the date changes
                                outfile.write('\n\n')
                            outfile.write(f'{date_str}\n')
                            previous_date = date_str
                            previous_sender = None  # Reset previous sender when date changes
                        
                        # Extract the sender and the message
                        sender, message = message_part.split(': ', 1)
                        
                        # Check if the sender has changed
                        if sender != previous_sender:
                            if previous_sender is not None:
                                # Write a blank line when the sender changes
                                outfile.write('\n')
                            previous_sender = sender
                        
                        # Write the formatted output
                        outfile.write(f'[{time_str}] {sender}:\n{message}')
                    
                    except ValueError:
                        # In case of a parsing error, skip the line (handle cases like line breaks)
                        continue

# Run the function
format_whatsapp_chat()
