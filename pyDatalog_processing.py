from pyDatalog import pyDatalog

pyDatalog.create_terms('X, Y, Z, Located_in, Water, Table, Dinner, Beer, Inmate, House, Car_show, Stuttgart, Western_hemisphere, Rubber_stamp, Health_center, Mouse_in_wall, result, Is_connected')

# 定义事实
+Located_in('Dinner', 'Table')
+Located_in('Water', 'Beer')
+Located_in('Inmate', 'House')
+Located_in('Rubber_stamp', 'Health_center')
+Located_in('Table', 'House')
+Located_in('Beer', 'Dinner')
+Located_in('Mouse_in_wall', 'House')
-Located_in('Water', 'Car_show')
-Located_in('Water', 'Stuttgart')
-Located_in('Water', 'Western_hemisphere')
-Located_in('Inmate', 'Health_center')

# 定义推理规则
# 基础规则: 如果X直接位于Y中，则它们是连接的
Is_connected(X,Y) <= Located_in(X,Y)

# 递归规则: 如果X位于Y，并且Y与Z连接，则X与Z也连接
Is_connected(X,Z) <= Located_in(X,Y) & Is_connected(Y,Z)

# 查询水是否与桌子连接
query_result = Is_connected('Water', 'Table')

# 根据查询结果输出
print(1 if query_result.data else 0)
