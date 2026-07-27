import pexpect
import sys
import time

def main():
    print("Starting agy CLI...")
    child = pexpect.spawn('agy run .agents/agents/lead-researcher.md --dangerously-skip-permissions', encoding='utf-8')
    child.logfile = sys.stdout
    
    print("Waiting for prompt 'for shortcuts'...")
    child.expect('for shortcuts', timeout=60)
    
    print("Prompt found. Waiting 2 seconds for TUI to settle...")
    time.sleep(2)
    
    print("Sending command...")
    child.sendline('Begin the research pipeline on the 100 apps in data/apps_list.json')
    
    print("Command sent. Now monitoring indefinitely...")
    try:
        child.expect(pexpect.EOF, timeout=None)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
