local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local BASE_URL = "https://robloxtest-2h1p.onrender.com" -- Change this!

while true do
	for _, player in pairs(Players:GetPlayers()) do
		-- 1. Check if they need to verify
		local success, response = pcall(function()
			return HttpService:GetAsync(BASE_URL .. "/get_status/" .. player.Name)
		end)

		if success then
			local data = HttpService:JSONDecode(response)
			if data.status == "unverified" then
				-- Display code to player (using a Hint for visibility)
				local hint = player.PlayerGui:FindFirstChild("VerifyHint") or Instance.new("Hint", player.PlayerGui)
				hint.Name = "VerifyHint"
				hint.Text = "Your Python Verification Code is: " .. data.code
			else
				-- If verified, clear hint and check for messages
				local hint = player.PlayerGui:FindFirstChild("VerifyHint")
				if hint then hint:Destroy() end
				
				local msgSuccess, msgResp = pcall(function()
					return HttpService:GetAsync(BASE_URL .. "/poll/" .. player.Name)
				end)
				
				if msgSuccess then
					local msgData = HttpService:JSONDecode(msgResp)
					if msgData.message then
						print("[" .. player.Name .. "]: " .. msgData.message)
					end
				end
			end
		end
	end
	task.wait(2)
end