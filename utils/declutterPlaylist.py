# python .\freeiptv.ottc.xyz.py .\tv_channels_098768842155_plus.m3u output.m3u 098768842155 975226199472s
import re
import argparse

blacklisted_languages = ["FR", "DE", "IR", "BN", "AR", "TN", "TL", "KL", "GR", "NL", "ML", "EX", "PL", "LA", "SE", "KANNADA", "TELUGU", "TELEGU", "ES"]

def declutter_playlist(input_filepath, output_filepath, url_part1=None, url_part2=None):
    """
    Parses an M3U file, filters entries based on 'group-title',
    and modifies URLs for the remaining entries.
    """
    try:
        # Read all lines from the input file into memory
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            lines = infile.readlines() 
            
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            # Ensure the output file starts with #EXTM3U
            # Check if the first line of the input is #EXTM3U (case-insensitive)
            if lines and lines[0].strip().upper() == "#EXTM3U":
                outfile.write(lines[0]) # Write original header line
                start_index = 1         # Start processing from the next line
            else:
                outfile.write("#EXTM3U\n") # Add header if missing or different
                start_index = 0         # Process all lines from the beginning

            i = start_index
            while i < len(lines):
                current_line_raw = lines[i]
                current_line_stripped = current_line_raw.strip()

                # Check if the current line is an #EXTINF directive
                if current_line_stripped.startswith("#EXTINF:"):
                    extinf_line_raw = current_line_raw # Store the #EXTINF line
                    
                    # Check if there's a next line for the URL
                    if i + 1 < len(lines):
                        url_line_raw = lines[i+1] # This should be the URL line
                        url_line_stripped = url_line_raw.strip()

                        # Default to keeping the entry
                        keep_entry = True
                        
                        # Parse group-title from extinf_line_raw
                        # Regex to find group-title="...", case insensitive for "group-title" attribute name
                        group_title_match = re.search(r'group-title="([^"]*)"', extinf_line_raw, re.IGNORECASE)
                        
                        if group_title_match:
                            group_title_value = group_title_match.group(1)
                            forbidden_substrings = blacklisted_languages
                            # Case-insensitive check for forbidden substrings in the group-title value
                            if any(sub.lower() in group_title_value.lower() for sub in forbidden_substrings):
                                keep_entry = False
                        
                        if keep_entry:
                            # Write the #EXTINF line
                            outfile.write(extinf_line_raw)

                            # Process and write the URL line
                            modified_url_to_write = url_line_raw # Default to original URL line

                            # Attempt to modify if it looks like a URL and contains '/live/'
                            # Check for "://" to ensure it's a URL structure and "/live/" for the specific path part
                            if url_part1 and url_part2 and "://" in url_line_stripped and "/live/" in url_line_stripped.lower():
                                temp_parts = url_line_stripped.split('/')
                                live_segment_idx = -1
                                
                                # Find the index of the "live" segment (case-insensitive search for "live")
                                for idx, part in enumerate(temp_parts):
                                    if part.lower() == "live":
                                        live_segment_idx = idx
                                        break
                                
                                # Check if "live" was found and if there are enough segments after it to modify
                                if live_segment_idx != -1 and live_segment_idx + 2 < len(temp_parts):
                                    temp_parts[live_segment_idx + 1] = url_part1
                                    temp_parts[live_segment_idx + 2] = url_part2
                                    
                                    reconstructed_url_content = "/".join(temp_parts)
                                    
                                    # Preserve original newline character(s) to maintain file integrity
                                    if url_line_raw.endswith('\r\n'): # Windows-style newline
                                        modified_url_to_write = reconstructed_url_content + '\r\n'
                                    elif url_line_raw.endswith('\n'): # Unix-style newline
                                        modified_url_to_write = reconstructed_url_content + '\n'
                                    else: # No newline at the end of the original line
                                        modified_url_to_write = reconstructed_url_content
                                else:
                                    # "live" not found or URL structure after "live" is not as expected for modification.
                                    # The original URL will be written. A warning could be printed here if desired.
                                    # print(f"Warning: URL format issue or 'live' segment not structured for modification: {url_line_stripped}")
                                    pass 
                            
                            outfile.write(modified_url_to_write)
                        
                        i += 2 # Processed #EXTINF and URL, so advance by 2 to get to the next pair
                        continue 
                    else:
                        # #EXTINF line at the end of the file without a corresponding URL line.
                        # This entry is incomplete. Current behavior: discard by not writing and advancing.
                        # print(f"Warning: #EXTINF line found at end of file without a URL: {extinf_line_raw.strip()}")
                        i += 1 # Advance past this incomplete #EXTINF line
                        continue
                else:
                    # This line is not an #EXTINF line.
                    # It could be a comment (e.g., #EXTVLCOPT), other metadata, or an empty line.
                    # Write it to the output if it's not an empty line (after stripping).
                    if current_line_stripped: 
                        outfile.write(current_line_raw)
                    # If it was an empty line (just newline characters), it will be skipped.
                    i += 1 # Advance to the next line
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_filepath}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Filters an M3U playlist based on 'group-title' and modifies stream URLs.",
        formatter_class=argparse.RawTextHelpFormatter, # For better help text formatting
        epilog="""
Example usage:
  python your_script_name.py input.m3u output.m3u NEW_PART_A NEW_PART_B

This will:
1. Read 'input.m3u'.
2. Filter out entries where 'group-title' contains 'FR', 'DE', or 'IR' (case-insensitive).
3. For remaining entries, modify URLs like 'scheme://host/live/old1/old2/stream.ts'
   to 'scheme://host/live/NEW_PART_A/NEW_PART_B/stream.ts'.
4. Write the result to 'output.m3u'.
"""
    )
    parser.add_argument("input_file", help="Path to the input .m3u file.")
    parser.add_argument("output_file", help="Path to the output .m3u file.")
    parser.add_argument("url_part1", help="The first segment to replace in the URL path after '/live/'.")
    parser.add_argument("url_part2", help="The second segment to replace in the URL path after '/live/url_part1/'.")
    
    args = parser.parse_args()
    
    declutter_playlist(args.input_file, args.output_file, args.url_part1, args.url_part2)
    print(f"Processing complete. Output written to '{args.output_file}'.")

if __name__ == "__main__":
    main()
