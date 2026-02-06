local HttpService = game:GetService("HttpService")
local ServerStorage = game:GetService("ServerStorage")
local TextChatService = game:GetService("TextChatService")

-- Path changed to ServerStorage for security
local config = ServerStorage:WaitForChild("ServerConfig")
local URL = config:WaitForChild("ApiUrl").Value

local lastMsgCount = 0
local isConnected = false

local function updateGui(player, code)
	local gui = player.PlayerGui:FindFirstChild("AuthGui") or Instance.new("ScreenGui", player.PlayerGui)
	gui.Name = "AuthGui"
	
	local frame = gui:FindFirstChild("Frame") or Instance.new("Frame", gui)
	frame.Name = "Frame"
	frame.Size = UDim2.new(0.3, 0, 0.1, 0)
	frame.Position = UDim2.new(0.35, 0, 0.05, 0)
	frame.BackgroundColor3 = Color3.new(0,0,0)
	frame.BackgroundTransparency = 0.3
	
	local label = frame:FindFirstChild("Label") or Instance.new("TextLabel", frame)
	label.Name = "Label"
	label.Size = UDim2.new(1, 0, 1, 0)
	label.BackgroundTransparency = 1
	label.TextColor3 = Color3.new(1,1,1)
	label.Font = Enum.Font.GothamBold
	label.TextScaled = true 
	label.Text = "AUTH CODE: " .. code
end

-- Function to handle Bubble Chat
local function createBubble(username, content)
	local player = game.Players:FindFirstChild(username)
	if player and player.Character and player.Character:FindFirstChild("Head") then
		-- This creates the overhead bubble
		TextChatService:DisplayBubble(player.Character.Head, content)
	end
end

task.spawn(function()
	print("📡 Initializing Python Server Link...")
	
	while true do
		local names = {}
		for _, p in pairs(game.Players:GetPlayers()) do table.insert(names, p.Name) end
		
		local success, response = pcall(function()
			return HttpService:PostAsync(URL .. "/roblox_sync", HttpService:JSONEncode({players = names}))
		end)

		if success then
			if not isConnected then
				print("✅ Python Server Connected!")
				isConnected = true
			end
			
			local data = HttpService:JSONDecode(response)
			
			-- 1. Manage Auth GUIs
			for _, p in pairs(game.Players:GetPlayers()) do
				local session = data.sessions[p.Name]
				if session and session.status == "pending" then
					updateGui(p, session.code)
				elseif p.PlayerGui:FindFirstChild("AuthGui") then
					p.PlayerGui.AuthGui:Destroy()
				end
			end
            
			-- 2. Handle Messages as Bubble Chat
			if #data.messages > lastMsgCount then
				for i = lastMsgCount + 1, #data.messages do
					local fullMsg = data.messages[i] -- Format: "Username: Message"
					local split = string.split(fullMsg, ": ")
					local user, content = split[1], split[2]
					
					if user and content then
						print("[Python Sync]: " .. fullMsg)
						createBubble(user, content)
					end
				end
				lastMsgCount = #data.messages
			end
		else
			if isConnected then
				warn("❌ Python Server Disconnected!")
				isConnected = false
			end
		end
		task.wait(1.5)
	end
end)