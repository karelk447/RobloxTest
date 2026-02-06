local HttpService = game:GetService("HttpService")
local URL = "https://your-app-name.onrender.com"

local lastProcessedMsg = 0

-- Helper to manage UI
local function updateUI(username, code)
	local player = game.Players:FindFirstChild(username)
	if not player then return end
	
	local gui = player.PlayerGui:FindFirstChild("VerificationGui")
	if not gui then
		gui = Instance.new("ScreenGui", player.PlayerGui)
		gui.Name = "VerificationGui"
		local label = Instance.new("TextLabel", gui)
		label.Size = UDim2.new(0, 400, 0, 80)
		label.Position = UDim2.new(0.5, -200, 0.1, 0)
		label.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
		label.TextColor3 = Color3.fromRGB(255, 255, 255)
		label.TextSize = 25
		label.BorderSizePixel = 3
	end
	gui.TextLabel.Text = "PYTHON AUTH CODE: " .. (code or "---")
end

-- Long Polling Loop
task.spawn(function()
	while true do
		local success, result = pcall(function()
			return HttpService:GetAsync(URL .. "/poll_updates")
		end)

		if success then
			local data = HttpService:JSONDecode(result)
			
			-- 1. Sync UI/Verifications
			for _, player in pairs(game.Players:GetPlayers()) do
				local sessionData = data.verifications[player.Name]
				if sessionData and sessionData.status == "pending" then
					updateUI(player.Name, sessionData.code)
				else
					local gui = player.PlayerGui:FindFirstChild("VerificationGui")
					if gui then gui:Destroy() end
				end
			end
			
			-- 2. Sync Messages (Instant)
			if #data.messages > lastProcessedMsg then
				for i = lastProcessedMsg + 1, #data.messages do
					print("[Python Sync]: " .. data.messages[i])
				end
				lastProcessedMsg = #data.messages
			end
		end
		task.wait(0.1)
	end
end)