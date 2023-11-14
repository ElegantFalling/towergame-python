extends Sprite2D

var Wall = preload("res://Wall/Wall.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	var screen_x = get_viewport_rect().size.x
	var screen_y = get_viewport_rect().size.y
	var smaller_dim = min(screen_x, screen_y)
	for i in range(floor(smaller_dim/50)):
		for j in range(floor(smaller_dim/50)):
			var new_wall = Wall.instantiate()
			new_wall.position = Vector2(i*50+25,j*50+25)
			add_child(new_wall)
			


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
