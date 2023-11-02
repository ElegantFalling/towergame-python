extends Node2D

var Wall = preload("res://Wall/Wall.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
	
func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
			var wall_instance = Wall.instantiate()
			wall_instance.position = event.position
			wall_instance.position = wall_instance.position.snapped(Vector2(50,50))
			add_child(wall_instance)
			var tower = get_node("Tower")
			print("World Tower: ", tower.get_rect())
			print("World Wall: ", wall_instance.get_rect())
			print("World Click: ", to_local(event.position))
			if tower.get_rect().has_point((to_local(event.position))):
				print("Free me!!")
				wall_instance.queue_free()
			
