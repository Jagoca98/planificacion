classdef Node
    properties
        x
        y
        myId
        parentId
    end
    methods
        function obj = Node(x, y, myId, parentId)
            obj.x = x;
            obj.y = y;
            obj.myId = myId;
            obj.parentId = parentId;
        end
        function dump(obj)
            fprintf("---------- x %d, y %d, id %d, pid %d\n",obj.x,obj.y,obj.myId,obj.parentId);
        end
    end
end
