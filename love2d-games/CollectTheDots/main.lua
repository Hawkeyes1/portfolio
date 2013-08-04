function my_setup()
    Nlines = 10
    Ndots = 10
    lines = {}
    dots = {}
    dotRadius = 3
    dotSpeed = 40
    victory = false
    victoryDistance = 5
    lineDistance2=25
    unpaused = false
    t = 0
    math.randomseed(os.time())
    for i=1,Nlines do
        x1 = math.random(0,width)
        y1 = math.random(0,height)
        x2 = x1 + (math.random(0,1)*2-1)*math.random(20,40)
        y2 = y1 + (math.random(0,1)*2-1)*math.random(20,40)
        table.insert(lines,{x1=x1,x2=x2,y1=y1,y2=y2})
    end
    for i=1,Ndots do
        x = math.random(0,width)
        y = math.random(0,height)
        table.insert(dots,{x=x,y=y})
    end
end

function love.load()
    width, height = 400,400
    success = love.graphics.setMode( width, height )
    if not success then
        os.exit()
    end
    my_setup()
end

function user_action()
    if victory then
        my_setup()
    else
        unpaused = not unpaused
    end
end

function love.keypressed(key)
    user_action()
end

function love.mousepressed( x, y, button )
    user_action()
end

function love.draw()
    love.graphics.setColor(255,0,0)
    for k,d in pairs(dots) do
        love.graphics.circle("fill",d.x,d.y,dotRadius)
        --love.graphics.print(k,d.x,d.y)
    end
    love.graphics.setColor(255,255,255)
    for k,r in pairs(lines) do
        love.graphics.line(r.x1,r.y1,r.x2,r.y2)
        --love.graphics.print(k,r.x1,r.y1)
    end
    if victory then
        love.graphics.print("VICTORY\nany key to reset",width/2,height/2)
    end
    love.graphics.print(t,20,20)
end
    
function is_obstructed(x1,y1,x2,y2,xp,yp,xm,ym)
    length2 = (x2-x1)^2 + (y2-y1)^2
    a = ((xp-x1)*(x2-x1) + (yp-y1)*(y2-y1))/length2
    xproj = x1 + a*(x2-x1)
    yproj = y1 + a*(y2-y1)
    n1, n2 = y2-y1,x1-x2
    if ((xproj - xp)^2 + (yproj - yp)^2) < lineDistance2 and a > 0 and a < 1 and not same_sign(n1*(xp-x1) + n2*(yp-y1),n1*(xm-x1) + n2*(ym-y1)) then
        return true
    else
        return false
    end
end

function same_sign(x,y)
    return (x >= 0 and y >= 0) or (x <= 0 and y <= 0)
end

function love.update(dt)
    if unpaused and not victory then
        t = t + dt
        x,y = love.mouse.getX(), love.mouse.getY()
        for k1,d in pairs(dots) do
            obstructed = false
            for k2,r in pairs(lines) do
                -- project d onto r
                if is_obstructed(r.x1,r.y1,r.x2,r.y2,d.x,d.y,x,y) then
                    --print(k1,k2)
                    obstructed = true
                end
            end
            if not obstructed then
                deltax, deltay = x - d.x, y - d.y
                norm = math.sqrt(deltax^2 + deltay^2)
                deltax, deltay = dotSpeed*dt*deltax/norm, dotSpeed*dt*deltay/norm
                d.x = d.x + deltax
                d.y = d.y + deltay
            end
        end
        victory = true
        for k,d in pairs(dots) do
            norm = math.sqrt((x - d.x)^2 + (y - d.y)^2)
            if norm > victoryDistance then
                victory = false
            end
        end
    end
end
