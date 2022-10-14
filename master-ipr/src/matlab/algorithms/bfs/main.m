FILE_NAME = "/usr/local/share/master-ipr/map1/map1.csv";
START_X = 2+1;
START_Y = 2+1;
END_X = 7+1;
END_Y = 2+1;

init = Node(START_X, START_Y, 0, -2);
% init.dump();

nodes = init;

intMap = csvread(FILE_NAME);

intMap(START_X, START_Y) = 3;
intMap(END_X, END_Y) = 4;

disp(intMap);

done = false;
goalParentId = -1;

while(~done)
    fprintf("--------------------- number of nodes: %d\n",length(nodes));
    for node = nodes
        node.dump;

        % up
        tmpX = node.x - 1;
        tmpY = node.y;
        if( intMap(tmpX, tmpY) == 4 )
            disp("up: GOALLLL!!!");
            goalParentId = node.myId;
            done = true;
            break
        elseif ( intMap(tmpX, tmpY) == 0 )
            disp("up: mark visited");
            newNode = Node(tmpX, tmpY, length(nodes), node.myId);
            intMap(tmpX, tmpY) = 2;
            nodes = [nodes newNode];
        end

        % down
        tmpX = node.x + 1;
        tmpY = node.y;
        if( intMap(tmpX, tmpY) == 4 )
            disp("down: GOALLLL!!!");
            goalParentId = node.myId;
            done = true;
            break
        elseif ( intMap(tmpX, tmpY) == 0 )
            disp("down: mark visited");
            newNode = Node(tmpX, tmpY, length(nodes), node.myId);
            intMap(tmpX, tmpY) = 2;
            nodes = [nodes newNode];
        end

        % right
        tmpX = node.x;
        tmpY = node.y + 1;
        if( intMap(tmpX, tmpY) == 4 )
            disp("right: GOALLLL!!!");
            goalParentId = node.myId;
            done = true;
            break
        elseif ( intMap(tmpX, tmpY) == 0 )
            disp("right: mark visited");
            newNode = Node(tmpX, tmpY, length(nodes), node.myId);
            intMap(tmpX, tmpY) = 2;
            nodes = [nodes newNode];
        end

        % left
        tmpX = node.x;
        tmpY = node.y - 1;
        if( intMap(tmpX, tmpY) == 4 )
            disp("left: GOALLLL!!!");
            goalParentId = node.myId;
            done = true;
            break
        elseif ( intMap(tmpX, tmpY) == 0 )
            disp("left: mark visited");
            newNode = Node(tmpX, tmpY, length(nodes), node.myId);
            intMap(tmpX, tmpY) = 2;
            nodes = [nodes newNode];
        end

        disp(intMap);
    end
end

disp("%%%%%%%%%%%%%%%%%%%");

ok = false;
while(~ok)
    for node = nodes
        if( node.myId == goalParentId )
            node.dump();
            goalParentId = node.parentId;
            if( goalParentId == -2)
                disp("%%%%%%%%%%%%%%%%%2");
                ok = true;
            end
        end
    end
end
