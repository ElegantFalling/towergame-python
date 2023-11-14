extends Sprite2D

var built = false

# Called when the node enters the scene tree for the first time.
func _ready():
	visible = not visible


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
		

func _input(event):
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if get_rect().has_point(event.position):
			built = true
			visible = not visible
			modulate = Color(255, 255, 0)

func _on_area_2d_mouse_entered():
	if not built:
		visible = not visible
	modulate = Color(0, 255, 0)


func _on_area_2d_mouse_exited():
	if not built:
		visible = not visible
	modulate = Color(255,255,0)
