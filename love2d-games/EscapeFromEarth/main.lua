function love.load()
    level1setup()
end

function level1setup()
    t = 0
    score = 0
    lives = 2
    level = 1
    
    clouds = {}
    stars = {}

    player = {x = 200, y = 400,
              ammo = 0, maxammo = 5, recharge = 1}
    
    blasts = {}
    bullets = {}
    
    asteroids = {}
    dust = {}
end

function love.draw()
    if lives >= 0 and level == 1 then
        level1draw()
    end
    if level == 2 then
        level2draw()
    end
    if lives == -1 then
        deaddraw()
    end
end

function level1draw()
    -- Background (sky blue fading to black)
    local d = math.min(t/300,1)
    love.graphics.setBackgroundColor((1-d)*135,(1-d)*206,(1-d)*250)
    
    -- Advice at level start
    if t < 5 then
        love.graphics.setColor(255,255,255)
        love.graphics.print("Escape the falling asteroids!\n\nMove with arrow keys.\nShoot with x, blast with z.",50,500)
    end
    
    -- Clouds
    love.graphics.setColor(211,211,211)
    function cloud(v)
        love.graphics.circle("fill",v.x,v.y,3*v.r)
        love.graphics.circle("fill",v.x-3*v.r,v.y+v.r,2*v.r)
        love.graphics.circle("fill",v.x+2*v.r,v.y+2*v.r,v.r)
        love.graphics.circle("fill",v.x+3*v.r,v.y-2*v.r,v.r)
    end
    map(clouds,cloud)
    
    -- Stars
    love.graphics.setColor(255,255,255)
    love.graphics.setLineWidth(2)
    function star(v)
        love.graphics.line(v.x-v.r,v.y-v.r,v.x+v.r,v.y+v.r)
        love.graphics.line(v.x-v.r,v.y+v.r,v.x+v.r,v.y-v.r)
    end
    map(stars,star)

    -- Progress bar
    love.graphics.setColor(0,255,0)
    love.graphics.setLineWidth(4)
    love.graphics.line(2,100,2,100*(1-d))
    
    -- Ammo bar
    love.graphics.setColor(255,69,0)
    love.graphics.setLineWidth(4)
    love.graphics.line(6,100,6,100 - 100*(player.ammo/player.maxammo))
    
    -- Lives
    love.graphics.setColor(255,255,255)
    for i=1,lives do
        love.graphics.triangle("fill",i*8-8,110,i*8,110,i*8-4,100)
    end
    --love.graphics.setColor(255,69,0)
    --love.graphics.triangle("fill",player.x-4,player.y,player.x+4,player.y,player.x,player.y+10)
    
    -- Score
    if t < 100 then love.graphics.setColor(0,0,0) else
        love.graphics.setColor(255,255,255) end
    love.graphics.print(score,0,110)
    
    -- Blasts
    love.graphics.setLineWidth(2)
    love.graphics.setColor(255,0,0)
    function blast(v)
        love.graphics.circle("line",v.x,v.y,400*(t-v.t),50)
    end
    map(blasts,blast)
    
    -- Bullets
    love.graphics.setColor(255,0,0)
    function bullet(v)
        love.graphics.circle("fill",v.x,v.y,2)
    end
    map(bullets,bullet)
    
    
    -- Player ship
    love.graphics.setColor(255,255,255)
    love.graphics.triangle("fill",player.x-8,player.y,player.x+8,player.y,player.x,player.y-20)
    love.graphics.setColor(255,69,0)
    love.graphics.triangle("fill",player.x-4,player.y,player.x+4,player.y,player.x,player.y+10)
    
    -- Asteroids
    love.graphics.setColor(139,69,19)
    function asteroid(v)
        love.graphics.circle("fill",v.x,v.y,v.r,30)
    end
    map(asteroids,asteroid)

    -- Dust
    function drawdust(v)
        local r = v.t-t
        if d > .5 then 
            love.graphics.setColor(r*255,0,0)
        else 
            love.graphics.setColor(255,(1-r)*255,(1-r)*255)
        end
        for i,p in pairs(v.points) do
            love.graphics.circle("fill",p.x,p.y,2,4)
        end
    end
    map(dust,drawdust)
        
end

function level2draw()
    love.graphics.setBackgroundColor(0,0,0)
    love.graphics.setColor(255,255,255)
    love.graphics.print("Game complete!\nPress r to restart.\nScore:"..score,0,100)

end

function deaddraw()
    love.graphics.setBackgroundColor(0,0,0)
    love.graphics.setColor(255,255,255)
    love.graphics.print("You have died.\nPress r to restart.",0,100)

end

function love.update(dt)
    if lives >= 0 and level == 1 then
        level1update(dt)
    end
end

function level1update(dt)
    -- Update time
    t = t + dt
    local d = math.min(t/300,1)
    if t > 300 then
        level = 2
    end
    
    
    -- Resupply ammo
    if player.ammo < player.maxammo then
        player.ammo = math.min(player.maxammo,player.ammo + player.recharge * dt)
    end
    
    -- Spawn clouds/stars
    local r = 2
    if d < .4 then
        if math.random() < r*dt then
            table.insert(clouds,{x=math.random(0,300),y=0,r=math.random(2,5)})
        end
    else
        if math.random() < r*dt then
            table.insert(stars,{x = math.random(0,300), y = 0, r = math.random(2,7)})
        end
    end
    
    -- Move clouds/stars
    function move(e) e.y = e.y + 100*dt end
    map(clouds,move)
    map(stars,move)
    
    -- Cleanup clouds/stars
    function within(e) return e.y < 620 end
    clouds = filter(clouds,within)
    stars = filter(stars,within)
    
    -- Cleanup blasts
    function valid(e) return (t  < (e.t + .25)) end
    blasts = filter(blasts,valid)
    
    -- Move ship
    if love.keyboard.isDown("left") and player.x > 10 then
        player.x = player.x - 150* dt
    elseif love.keyboard.isDown("right") and player.x < 290 then
        player.x = player.x + 150*dt
    end
    if love.keyboard.isDown("up") and player.y > 20 then
        player.y = player.y - 150* dt
    elseif love.keyboard.isDown("down") and player.y < 590 then
        player.y = player.y + 150*dt
    end
    
    -- Move bullets
    function move(v) v.y = v.y - 400*dt end
    map(bullets,move)
    
    -- Cleanup bullets
    function inside(v) return (v.y > -20) end
    bullets = filter(bullets,inside)
    
    -- Spawn asteroids
    r = .5 + 2.5*d
    if math.random() < r*dt then
        table.insert(asteroids,{x=math.random(0,300),y=0,r=10+3*math.random(0,3)})
        score = score + 1
    end
    
    -- Move asteroids
    function move(e) e.y = e.y + 200*dt end
    map(asteroids,move)
    
    -- Cleanup offscreen asteroids
    function inside(v) if v.y < 620 then return 1 else score = score - 2; return nil end end
    asteroids = filter(asteroids,inside)
    
    -- Collide player/asteroids
    function collide(a)
        if math.sqrt((player.x-a.x)^2 + (player.y-8-a.y)^2) < a.r + 10 then
            lives = lives - 1
            return nil
        else
            return 1
        end
    end
    asteroids = filter(asteroids,collide)
    
    -- Collide asteroids/blasts
    for i,b in pairs(blasts) do
        local br = 400*(t-b.t)
        function collide(a)
            if math.sqrt((b.x-a.x)^2+(b.y-a.y)^2) > a.r + br then
                return 1
            else
                table.insert(dust,{t=t+1,points=dustpoints(a.x,a.y,a.r)})
                return nil
            end
        end
        asteroids = filter(asteroids,collide)
    end
    
    -- Collide asteroids/bullets
    for i,b in pairs(bullets) do
        function collide(a)
            if math.sqrt((a.x-b.x)^2 + (a.y-b.y)^2) > a.r + 2 then
                return 1
            else
                table.insert(dust,{t=t+1,points=dustpoints(a.x,a.y,a.r)})
                return nil
            end
        end
        result = filtered(asteroids,collide)
        asteroids = result[1]
        tossed = result[2]
        if tossed then
            table.remove(bullets,i)
        end
    end

    -- Cleanup dust
    function valid(v) return t < v.t  end
    dust = filter(dust,valid)

end

function love.keyreleased(key)
    if key == "z" then
        if player.ammo > 1 then
            player.ammo = player.ammo - 1
            table.insert(blasts,{x=player.x,y=player.y,t=t})
        end
    elseif key == "x" then
        if player.ammo > .35 then
            player.ammo = player.ammo - .35
            table.insert(bullets,{x=player.x,y=player.y-20})
        end
    elseif key == "r" and (lives == -1 or level == 2) then
        level1setup()
    end
    
end

function dustpoints(x,y,r)
    local points = {}
    for i=1,r do
        table.insert(points,{x=x+math.random(-2*r,2*r),
                             y=y+math.random(-2*r,2*r)})
    end
    return points
end
 -- Utility functions
 function map(t,fn)
    t2 = {}
    for k,v in pairs(t) do
        val = fn(v)
        table.insert(t2,val)
    end
    return t2
end

function filter(t,fn)
    t2 = {}
    for k,v in pairs(t) do
        if fn(v) then
            table.insert(t2,v)
        end
    end
    return t2
end

function filtered(t,fn)
    t2 = {}
    tossed = nil
    for k,v in pairs(t) do
        if fn(v) then
            table.insert(t2,v)
        else
            tossed = 1
        end
    end
    return {t2,tossed}
end

function setminus(a,b)
    -- return a setminus b
    c = {}
    for k,v in pairs(a) do
        if not contains(b,v) then
            table.insert(c,v)
        end
    end
    return c
end

function contains(t,v)
    for k,v2 in pairs(t) do
        if v2 == v then
            return true
        end
    end
    return false
end
