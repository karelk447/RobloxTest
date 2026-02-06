local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

-- REPLACE THIS with your actual Render URL
local BASE_URL = "https://robloxtest-2h1p.onrender.com/get/"

while true do
	for _, player in pairs(Players:GetPlayers()) do
		local url = BASE_URL .. player.Name
		
		local success, response = pcall(function()
			return HttpService:GetAsync(url)
		end)

		if success then
			local data = HttpService:JSONDecode(response)
			if data.message then
				-- This prints in the Roblox Output
				print("PYTHON SENDER [" .. player.Name .. "]: " .. data.message)
			end
		else
			warn("Failed to contact cloud server. It might be sleeping...")
		end
	end
	task.wait(3) -- Checking every 3 seconds
end