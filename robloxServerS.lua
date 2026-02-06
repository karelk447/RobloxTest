local HttpService = game:GetService("HttpService")
-- REPLACE THIS with your Render URL
local URL = "https://robloxtest-2h1p.onrender.com"

local lastProcessedMsgCount = 0

local function pollServer()
	while true do
		local success, response = pcall(function()
			return HttpService:GetAsync(URL .. "/get_updates")
		end)

		if success then
			local data = HttpService:JSONDecode(response)
			
			-- 1. Handle Messages (Only print new ones)
			if #data.messages > lastProcessedMsgCount then
				for i = lastProcessedMsgCount + 1, #data.messages do
					print("[Python Chat]: " .. data.messages[i])
				end
				lastProcessedMsgCount = #data.messages
			end
			
			-- 2. Keep track of pending verifications internally
			_G.PendingData = data.verifications
		else
			warn("Failed to contact Render server. It might be sleeping.")
		end
		task.wait(5) -- Poll every 5 seconds
	end
end

-- Watch for chat in-game
game.Players.PlayerAdded:Connect(function(player)
	player.Chatted:Connect(function(message)
		if _G.PendingData and _G.PendingData[player.Name] then
			local userStatus = _G.PendingData[player.Name]
			
			if userStatus.status == "pending" and message == userStatus.code then
				-- Notify Server
				local success = pcall(function()
					HttpService:PostAsync(URL .. "/confirm_roblox", 
						HttpService:JSONEncode({username = player.Name}),
						Enum.HttpContentType.ApplicationJson
					)
				end)
				if success then
					print(player.Name .. " has successfully verified!")
				end
			end
		end
	end)
end)

task.spawn(pollServer)