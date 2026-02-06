local HttpService = game:GetService("HttpService")
-- Fetches the link from the StringValue we created
local URL = game.ServerStorage:WaitForChild("ServerConfig"):WaitForChild("ApiUrl").Value

local lastMsgCount = 0

local function updateGui(player, code)
	local gui = player.PlayerGui:FindFirstChild("AuthGui") or Instance.new("ScreenGui", player.PlayerGui)
	gui.Name = "AuthGui"

	local frame = gui:FindFirstChild("Frame") or Instance.new("Frame", gui)
	frame.Name = "Frame"
	frame.Size = UDim2.new(0.3, 0, 0.1, 0)
	frame.Position = UDim2.new(0.35, 0, 0.05, 0)
	frame.BackgroundColor3 = Color3.new(0,0,0)

	local label = frame:FindFirstChild("Label") or Instance.new("TextLabel", frame)
	label.Name = "Label"
	label.Size = UDim2.new(1, 0, 1, 0)
	label.BackgroundTransparency = 1
	label.TextColor3 = Color3.new(1,1,1)
	label.TextScaled = true -- FIXED: Auto-resizing text
	label.Text = "AUTH CODE: " .. code
end

task.spawn(function()
	while true do
		local names = {}
		for _, p in pairs(game.Players:GetPlayers()) do table.insert(names, p.Name) end

		local success, response = pcall(function()
			return HttpService:PostAsync(URL .. "/roblox_sync", HttpService:JSONEncode({players = names}))
		end)

		if success then
			local data = HttpService:JSONDecode(response)
			for _, p in pairs(game.Players:GetPlayers()) do
				local session = data.sessions[p.Name]
				if session and session.status == "pending" then
					updateGui(p, session.code)
				elseif p.PlayerGui:FindFirstChild("AuthGui") then
					p.PlayerGui.AuthGui:Destroy()
				end
			end
			if #data.messages > lastMsgCount then
				for i = lastMsgCount + 1, #data.messages do
					print("[Python Sync]: " .. data.messages[i])
				end
				lastMsgCount = #data.messages
			end
		else
			warn("Server not responding")
		end
		task.wait(1.5)
	end
end)