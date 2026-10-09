if self.claw.state == Claw.EXTENDING:
    tip = self.claw.tip()
    for obj in self.level.objects:
        if obj.grabbable and not obj.destroyed and obj.collides_with(tip[0], tip[1], 6):
            obj.on_grab(self)
            if not obj.destroyed:
                self.claw.attach(obj)
                self.sounds.play("grab")
            else:
                self.claw.state = Claw.RETRACTING
            break