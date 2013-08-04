-- done: mover movement logic (at least while no guns can affect that)
-- done: display logic (at least while there are only planets, guns, lasers, endzones, movers)
-- to do: improve gun shooting logic?
-- to do: write and balance more levels
-- done: gun creation logic
-- done: gun types
-- done: enemy types

-- #########################
-- BASIC OUTLINE OF PROGRAM
-- #########################
-- We initialize some data.
-- Then, start in mode introduction.
-- User presses enter.
-- Alternate between playgame and placeguns



-- #########################
-- INITIALIZATION
-- #########################

function love.load()
  mode = 'introduction'
  love.graphics.setCaption("Defense")
  love.graphics.setMode(600,600)
  money = 100
  prevMoney = 100

-- #########################
-- LEVELS
-- #########################

numLevels = 3

function setUpLevel(level)
  guns = {}
  lasers = {}
  money = prevMoney
  if level == 1 then
    planets = {
      {x = 250, y = 200, w = 50, h = 50},
      {x = 450, y = 200, w = 50, h = 50},
      {x = 250, y = 400, w = 50, h = 50},
      {x = 450, y = 400, w = 50, h = 50},
      {x = 100, y = 300, w = 50, h = 50}
    }
    movers = {}
    for i=1,5 do
      for j=1,50 do
        table.insert(movers,{x = 50 + 10 * j, y = 20 + 10 * i, radius = 2, speed = 20, hp = 4, r = 0,g=200,b=80, bounty=1})
      end
    end
  elseif level == 2 then
    planets = {
      {x = 100, y = 125, w = 50, h = 50},
      {x = 200, y = 225, w = 50, h = 50},
      {x = 300, y = 325, w = 50, h = 50},
      {x = 400, y = 425, w = 50, h = 50},
    }
    movers = {}
    for i=1,5 do
      for j=1,50 do
        table.insert(movers,{x = 50 + 10 * j, y = 20 + 10 * i, radius = 4, speed = 20, hp = 8, r = 0,g=200,b=80, bounty=2})
      end
    end
  elseif level == 3 then
    planets = {
      {x = 100, y = 125, w = 50, h = 350},
      {x = 275, y = 275, w = 50, h = 50},
      {x = 400, y = 125, w = 50, h = 350},
    }
    movers = {}
    for i=1,5 do
      for j=1,50 do
        table.insert(movers,{x = 50 + 10 * j, y = 20 + 10 * i, radius = 4, speed = 20, hp = 8, r = 0,g=200,b=80, bounty=2})
      end
    end
  end
  mode = 'placeGuns'
end


-- #########################
-- GUNS
-- #########################

-- normal guns will have a range, laser color, laser width (?), and delay
-- as well as an x and y position.  and a gun color, which i guess
-- can be the same as laser color.  although perhaps the guns should be
-- different polygons if they are different types?
-- the guns' "cooldown" variable has been renamed "time"

-- the above will implement types 1, 2, 3, 6.  4 needs special logic and animation,
-- as do 5 and 7.

-- the slowing gun should be implemented during enemy movement; check if they're in range
-- of a slowing gun and if so just do dx = 0.5*dx or whatever

-- splash damage will require another animation table, splashes, which we update and delete 
-- and draw from just as lasers (but only when a splash gun fires).  it will also require 
-- changing the damage update when a splash gun fires to damage nearby movers

-- lightning gun similar to above. add in additional lasers, damage additional movers

-- long range power up may not be a good idea i am thinking.  but if it were implemented, the
-- gun would have a "firing" time, and a "target" mover, and each frame we'd draw the laser
-- directly from the gun to the mover.  and we'd lower the mover's HP by some_rate * firing.
-- (this would give a quadratic powerup).  perhaps the laser would grow in width linearly
-- with firing as well.

-- i am now thinking that it may be better to keep a game simple. for instance,
-- put the interesting stuff in the planet and enemy layout, and just have a few simple guns
-- thus the strategy would be just allocating resources basically.

-- guntype should have a description string

-- a gunType should define the following:
-- description
-- range
-- price
-- delay
-- damage


currGunType=1
gunTypes = {
  {description = "basic gun", range = 100, price = 5, delay = 0.5, damage = 2},
  {description = "long range gun", range = 300, price = 20, delay = 0.5, damage = 2},
  {description = "powerful gun", range = 100, price = 20, delay = 0.5, damage = 6},
  {description = "rapid fire gun", range = 100, price = 20, delay = 0.1, damage = 2},
  {description = "ultimate gun", range = 300, price = 100, delay = 0.1, damage = 6}
}
numGunTypes = #gunTypes

-- #########################
-- ENEMIES
-- #########################

-- there will need to be special logic to handle the types
-- "speeds up halfway" and "spawns when killed"
-- ("invisible" will just be colored black)

-- movers must define the following:
-- r, g, b      
-- x, y         
-- radius       
-- bounty
-- hp

numEnemyTypes = 6
enemyTypes = {}
-- slow light
-- slow heavy
-- fast light
-- speeds up halfway
-- slow very heavy, spawns a fast light when killed
-- fast light + invisible


end



function obstructed(mov, ds)
  -- assumption: at most one planet obstructs a given mover
  for k, plt in pairs(planets) do
    -- the commented out parts here refer to a possible future change;
    -- namely, that planets could just implement a contains method,
    -- and tell a mover which direction to go on impact.
    -- if plt.contains(mov.x,mov.y + ds) then
    if plt.x <= mov.x and mov.x <= plt.x + plt.w and mov.y + ds >= plt.y then
      -- if plt.go_right(mov.x) then
      if plt.x + 0.5*plt.w <= mov.x then
        return 1
      else
        return -1
      end
    end
  end
  return false
end

function dist(x1,y1,x2,y2) 
  -- Euclidean distance in the plane
  return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
end

function purgeTable(t)
  -- remove all elements whose time has gone below 0
  toRemove = {}
  for k, v in pairs(t) do
    if v.time <= 0 then
      table.insert(toRemove,k)
    end
  end
  for k, v in pairs(toRemove) do
    table.remove(t,v)
  end
end

function updateTimes(t,dt)
  -- decrease all elements' times by dt
  for k, v in pairs(t) do
      v.time = v.time - dt
  end
end

-- #########################
-- MAIN GAME LOOP
-- #########################

function love.update(dt)
if mode == 'playGame' then
  -- update mover positions
  for k, v in pairs(movers) do
    ds = dt*v.speed
    obs = obstructed(v,ds)
    if obs then
      v.x = v.x + obs*ds
    else
      v.y = v.y + ds
    end
  end
  updateTimes(lasers,dt)
  purgeTable(lasers)
  updateTimes(guns,dt)
  -- guns shoot, create lasers
  for k, gun in pairs(guns) do
    if gun.time <= 0 then
      -- gun will shoot at the thing in range with biggest y-coordinate
      ycoord = 0
      moverKey = false
      for k2, mov in pairs(movers) do
        if mov.y >= ycoord and dist(gun.x,gun.y,mov.x,mov.y) <= gun.range then
          ycoord = mov.y
          moverKey = k2
          mover = mov
        end
      end
      if moverKey then
        gun.time = gun.delay
        mover.hp = mover.hp - gun.damage
        if mover.hp <= 0 then
          prevMoney = prevMoney + mover.bounty
          table.remove(movers,moverKey)
        end
        table.insert(lasers,{x1=gun.x, y1=gun.y, x2=mover.x, y2=mover.y, time=0.1, r=255, g=0, b=0})
      end
    end
  end
  -- remove winning movers
  winningMovers = {}
  for k, v in pairs(movers) do
    if v.y > 500 then
      table.insert(winningMovers,k)
    end
  end
  for k, v in pairs(winningMovers) do
    table.remove(movers,v)
  end
  if #movers == 0 then
    if level < numLevels then
      level = level + 1
      setUpLevel(level)
    else
      mode = "finished"
    end
  end
      
end
end

function validGunLocation(x, y)
  for k, plt in pairs(planets) do
    -- again, if the planets become more varied, we'd just have this:
    -- if plt.contains(x,y) then
    if plt.x <= x and plt.x + plt.w >= x and plt.y <= y and plt.y + plt.h >= y then
      return true
    end
  end
  return false
end

-- #########################
-- CALLBACKS
-- #########################

function love.mousereleased(x, y, button)
  gun = gunTypes[currGunType]
  if mode == 'placeGuns' and validGunLocation(x,y) and money >= gun.price then
    table.insert(guns,{x = x, y = y, time=0, range = gun.range, delay = gun.delay, damage = gun.damage})
    money = money - gun.price
  end
end

function love.keypressed(key, unicode)
  if mode == "placeGuns" then
    if key == "return" then
      mode = "playGame"
    elseif key == "up" and currGunType < numGunTypes then
      currGunType = currGunType + 1
    elseif key == "down" and currGunType > 1 then
      currGunType = currGunType - 1
    end
  elseif mode == "introduction" and key == "return" then
    level = 1
    setUpLevel(1)
  end
end

-- #########################
-- MAIN DRAW LOOP
-- #########################

function love.draw()
  if mode == 'introduction' then
    love.graphics.setColor(255,255,255)
    love.graphics.print("Each level, you will place guns, then your guns will defend.\nYou get money based on how well you defend.\nThere are "..numLevels.." levels. Press enter to begin.",50,50)
  end
  if mode == 'finished' then
    love.graphics.setColor(255,255,255)
    love.graphics.print("Last level completed.  Score: "..prevMoney,50,50)
  end
  if mode == 'placeGuns' or mode == 'playGame' then
    -- white planets
    love.graphics.setColor(255,255,255)
    for k, v in pairs(planets) do
      love.graphics.rectangle('fill',v.x,v.y,v.w,v.h)
    end
    -- orange endzones
    love.graphics.setColor(200,80,0)
    love.graphics.setLineWidth(2)
    love.graphics.line(0,100,600,100)
    love.graphics.line(0,500,600,500)
    -- blue guns 
    love.graphics.setColor(0,0,255)
    for k, v in pairs(guns) do
      love.graphics.circle('fill',v.x,v.y,2)
    end
    for k, v in pairs(movers) do
      love.graphics.setColor(v.r,v.g,v.b)
      love.graphics.circle('fill',v.x,v.y,v.radius)
    end
  end
  if mode == 'placeGuns' then
    -- money display
    love.graphics.setColor(255,255,255)
    love.graphics.print("Money: "..money..", click to place guns, enter to start.\nCurrent gun: "..currGunType..", up/down to change.\nPrice: "..gunTypes[currGunType].price..". "..gunTypes[currGunType].description,50,530)
    -- display blue gun radius about each gun
    love.graphics.setColor(0,0,255)
    for k, v in pairs(guns) do
      love.graphics.circle('line',v.x,v.y,v.range,30)
    end
    -- display red gun radius about pointer
    love.graphics.setColor(255,0,0)
    love.graphics.circle('line',love.mouse.getX(),love.mouse.getY(),gunTypes[currGunType].range,30)
  end
  if mode == 'playGame' then
    love.graphics.setColor(255,255,255)
    love.graphics.print("Money for next round: "..prevMoney,50,50)
    for k, v in pairs(lasers) do
      love.graphics.setColor(v.r,v.g,v.b)
      love.graphics.line(v.x1, v.y1, v.x2, v.y2)
    end
  end
end
