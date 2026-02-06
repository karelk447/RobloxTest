local HttpService = game:GetService("HttpService")
local URL = "https://robloxtest-2h1p.onrender.com"

-- Poll the server every 5 seconds for new info
task.spawn(function()
	while true do
		local success, response = pcall(function()
			return HttpService:GetAsync(URL .. "/get_updates")
		end)

		if success then
			local data = HttpService:JSONDecode(response)
			
			-- Handle Messages
			for _, msg in pairs(data.messages) do
				print("[Server Link]: " .. msg)
			end
			
			-- Check if anyone in-game is trying to verify
			game.Players.PlayerAdded:Connect(function(player)
				player.Chatted:Connect(function(message)
					local userVerifyData = data.verifications[player.Name]
					if userVerifyData and userVerifyData.status == "pending" then
						if message == userVerifyData.code then
							-- Tell the Python server they are good!
							HttpService:PostAsync(URL .. "/confirm_roblox", 
								HttpService:JSONEncode({username = player.Name}))
							print(player.Name .. " verified!")
						end
					end
				end)
			end)
		end
		task.wait(5)
	end
end)