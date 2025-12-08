**Exercise 1**

I added context7 MCP in Augment to add tests. This was very easy to set up and use.

**Exercise 2**

I am using Sqlite for the config service database.

After researching database MCPs for SQLite I found this [mcp-server-sqlite](https://mcp-get.com/packages/mcp-server-sqlite)  which provides an easy installation command.

However it didn't work straight away after installing it.

I found most of the MCP servers have instructions for other coding agents like Claude. 

I read about [Sequential Thinking MCP](https://mcpservers.org/servers/modelcontextprotocol/sequentialthinking) being popular so I also added this MCP in the Augment settings and I asked Augment:


```
how do I install and use mcp servers in Augment? use sequential thinking and context7

Sequential_thinking
sequentialthinking
Context_7
resolve-library-id
Sequential_thinking
sequentialthinking
Context_7
get-library-docs
Context_7
get-library-docs
Sequential_thinking
sequentialthinking
Context_7
get-library-docs
Sequential_thinking
sequentialthinking
Context_7
get-library-docs
Sequential_thinking
sequentialthinking
Context_7
get-library-docs
Sequential_thinking
sequentialthinking

Complete Guide: Installing and Using MCP Servers in Augment
Based on the official Augment documentation, here's everything you need to know about MCP servers:

📚 What Are MCP Servers?
MCP (Model Context Protocol) is an open protocol that allows Augment to connect to external tools and data sources. MCP servers provide:

Access to external data (databases, APIs, files)
Integration with tools (query databases, run tests, send messages)
Standardized connections to various systems
Once configured, I (the AI) can automatically use these tools to help you!

🔧 How to Install & Configure MCP Servers
You have two methods to configure MCP servers. Important: Servers configured via one method are NOT visible in the other, so stick with one approach.

Method 1: Augment Settings Panel (Recommended - Easiest)
Step 1: Open Augment Settings

Click the options menu (⋮) in the upper right of the Augment panel
Click "Settings"
Step 2: Add an MCP Server

Locate the MCP servers section
Click the "+" button next to the 'MCP' header
Fill in the fields:
Name: Unique server name (e.g., sqlite, mongodb)
Command: Command to run the server with arguments
Step 3: Manage Servers

Edit or delete: Click the "..." button next to the server name
Add more: Click the "+" button again
Step 4: Restart VS Code

Press Ctrl+Shift+P (or Cmd+Shift+P on Mac)
Type "Reload Window"
Select "Developer: Reload Window"
Method 2: Edit settings.json Directly
Step 1: Open settings.json

Open the command palette (Ctrl+Shift+P or Cmd+Shift+P)
Select "Edit Settings"
Under Advanced, click "Edit in settings.json"
Step 2: Add MCP Configuration

Add this structure to your settings.json:

Step 3: Save and Restart

Save the file
Restart VS Code (Command Palette → "Developer: Reload Window")
📝 Example Configurations
SQLite Database Server
Using Settings Panel:

Name: sqlite
Command: uvx mcp-server-sqlite --db-path /path/to/your/database.db
Using settings.json:

Prerequisites:

Install uv (Python package installer): pip install uv
The uvx command will automatically install mcp-server-sqlite when first run
Multiple Servers Example
🚀 How to Use MCP Servers
Once configured and VS Code is reloaded, you don't need to do anything special! Just ask me naturally:

Example Queries:
For SQLite MCP:

"How many items are in the database?"
"Show me all tables in the database"
"What's the schema of the users table?"
"Query all records where status is 'active'"
I'll automatically:

Detect that you're asking about the database
Use the appropriate MCP tool (e.g., read-query, list-tables)
Execute the query
Return the results to you
✅ Verifying Your MCP Server is Working
Check Server Status:
Open Augment Settings → MCP section
Look for your server in the list
Check for status indicators:
🟢 Green = Connected and working
🔴 Red = Error or not running
⚪ Gray = Not started
Test the Server:
Click the "..." menu next to your server
Select "Test"
This verifies the server can start and respond
🛠️ Troubleshooting
Problem: Server not showing up
Solution:

Restart VS Code (Ctrl+Shift+P → "Developer: Reload Window")
Check that you used the same configuration method (Settings Panel OR settings.json)
Problem: Command not found
Solution:

Ensure dependencies are installed (e.g., uv, python, node)
Use full paths to commands if needed
Problem: Database path errors
Solution:

Use absolute paths (e.g., C:\Users\username\project\database.db)
Ensure the database file exists
Check file permissions
Problem: Server configured but tools not available
Solution:

Restart VS Code completely
Check the Output panel for error messages
Verify the command runs successfully in your terminal first
🎯 Popular MCP Servers
Here are some commonly used MCP servers:

Server	Command	Purpose
SQLite	uvx mcp-server-sqlite	Query SQLite databases
Filesystem	npx @modelcontextprotocol/server-filesystem	Access local files
Brave Search	npx @modelcontextprotocol/server-brave-search	Web search
Puppeteer	npx @modelcontextprotocol/server-puppeteer	Browser automation
MongoDB	Custom server	Query MongoDB databases
📌 Key Takeaways
✅ Two configuration methods - Settings Panel (UI) or settings.json (file)
✅ Restart required - Always reload VS Code after configuration
✅ Automatic usage - Once configured, I use MCP tools automatically
✅ Unique names - Each server needs a unique name
✅ Dependencies - Ensure required tools (uvx, npx, python) are installed
✅ Absolute paths - Use full paths for database files and scripts
🎉 Ready to Get Started?
Pick a configuration method and try setting up your first MCP server! The SQLite example is a great place to start if you have a local database to query.

Need help with a specific MCP server? Just ask!
```

**Exercise 3**

I decided to try the Notion MCP as I sometimes use Notion for my personal organisation. I created a new page with some text and asked Augment about it.

Augment and the MCP could not read any "pages" but when I provided the URL `https://www.notion.so/2c3dfbce573c80b6aac2d7cab6ca4bc4?v=2c3dfbce573c80fabe82000c5149bc16` , it responded:

```

Perfect! Let me read that Notion page:

Notion
Read the AI Agents Course page
The URL you provided appears to be a database view rather than a page. Let me try reading it as a database:

Notion
Read the AI Agents Course database
Excellent! I can now access your Notion database. Here's what I found:

AI Agents Course Database
Database Details:

Created: December 8, 2025 at 9:57 PM
Last Updated: December 8, 2025 at 10:01 PM
Properties: Tags, Created
Pages in the Database:
1. Untitled
URL: View Page
Created: December 8, 2025 at 10:00 PM
Last Edited: December 8, 2025 at 10:00 PM
2. install Notion MCP
URL: View Page
Created: December 8, 2025 at 10:00 PM
Last Edited: December 8, 2025 at 10:00 PM
Summary
You have 2 pages in your AI Agents Course database:

An untitled page (needs a name)
A page about installing Notion MCP
Would you like me to read the content of either of these pages? I can show you what's inside the "install Notion MCP" page or the untitled one!
```