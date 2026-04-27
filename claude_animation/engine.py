import math
import random
import objc
from AppKit import (
    NSApplication, NSWindow, NSView, NSColor, NSBezierPath,
    NSMakeRect, NSBackingStoreBuffered, NSFloatingWindowLevel,
    NSWindowCollectionBehaviorCanJoinAllSpaces,
    NSWindowStyleMaskBorderless, NSRoundLineCapStyle, NSScreen, NSApp,
)
from Foundation import NSObject, NSTimer

W, H = 900, 500


class WhipView(NSView):
    _frame = None

    def isOpaque(self):
        return False

    def drawRect_(self, rect):
        NSColor.clearColor().set()
        NSBezierPath.fillRect_(self.bounds())
        if self._frame is None:
            return
        self._paint(self._frame)

    @objc.python_method
    def _paint(self, f):
        path = NSBezierPath.bezierPath()
        path.moveToPoint_((f['p0'][0], f['p0'][1]))
        path.curveToPoint_controlPoint1_controlPoint2_(
            (f['p3'][0], f['p3'][1]),
            (f['p1'][0], f['p1'][1]),
            (f['p2'][0], f['p2'][1]),
        )

        if f['crack']:
            path.setLineWidth_(f['lw'] + 16)
            NSColor.colorWithRed_green_blue_alpha_(1.0, 0.3, 0.0, 0.2).setStroke()
            path.stroke()
            path.setLineWidth_(f['lw'] + 8)
            NSColor.colorWithRed_green_blue_alpha_(1.0, 0.8, 0.0, 0.4).setStroke()
            path.stroke()

        path.setLineWidth_(f['lw'])
        path.setLineCapStyle_(NSRoundLineCapStyle)
        r, g, b = f['col']
        NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0).setStroke()
        path.stroke()

        hx, hy = f['p0']
        grip = NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(
            NSMakeRect(hx - 7, hy - 4, 14, 30), 3, 3
        )
        NSColor.colorWithRed_green_blue_alpha_(0.22, 0.10, 0.01, 0.95).setFill()
        grip.fill()
        NSColor.colorWithRed_green_blue_alpha_(0.55, 0.28, 0.05, 1.0).setStroke()
        grip.setLineWidth_(1.5)
        grip.stroke()

        if f['crack']:
            self._paint_crack(f['p3'])

    @objc.python_method
    def _paint_crack(self, tip):
        tx, ty = tip
        for rad, a, r, g, b in [
            (50, 0.45, 1.0, 0.40, 0.0),
            (32, 0.65, 1.0, 0.85, 0.0),
            (16, 0.90, 1.0, 1.00, 0.8),
            ( 7, 1.00, 1.0, 1.00, 1.0),
        ]:
            oval = NSBezierPath.bezierPathWithOvalInRect_(
                NSMakeRect(tx - rad, ty - rad, rad * 2, rad * 2)
            )
            NSColor.colorWithRed_green_blue_alpha_(r, g, b, a).setFill()
            oval.fill()

        rng = random.Random(42)
        for _ in range(16):
            angle = rng.uniform(0, 2 * math.pi)
            length = rng.uniform(35, 90)
            spark = NSBezierPath.bezierPath()
            spark.setLineWidth_(rng.uniform(1.0, 2.5))
            spark.moveToPoint_((tx, ty))
            spark.lineToPoint_((tx + length * math.cos(angle), ty + length * math.sin(angle)))
            NSColor.colorWithRed_green_blue_alpha_(1.0, 0.70, 0.0, 0.88).setStroke()
            spark.stroke()


class Animator(NSObject):
    def init(self):
        self = objc.super(Animator, self).init()
        self.idx = 0
        self.view = None
        self.win = None
        self.frames = None
        return self

    def start(self):
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.05, self, b'tick:', None, False
        )

    def tick_(self, timer):
        if self.idx >= len(self.frames):
            self.win.close()
            NSApp.terminate_(None)
            return
        f = self.frames[self.idx]
        self.view._frame = f
        self.view.setNeedsDisplay_(True)
        self.idx += 1
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            f['ms'] / 1000.0, self, b'tick:', None, False
        )


class AppDelegate(NSObject):
    frames = None

    def applicationDidFinishLaunching_(self, _notif):
        screen_rect = NSScreen.mainScreen().frame()
        sw = screen_rect.size.width
        sh = screen_rect.size.height
        x = (sw - W) / 2
        y = (sh - H) / 2

        win = NSWindow.alloc().initWithContentRect_styleMask_backing_deferred_(
            NSMakeRect(x, y, W, H),
            NSWindowStyleMaskBorderless,
            NSBackingStoreBuffered,
            False,
        )
        win.setLevel_(NSFloatingWindowLevel)
        win.setOpaque_(False)
        win.setBackgroundColor_(NSColor.clearColor())
        win.setIgnoresMouseEvents_(True)
        win.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)
        win.setHasShadow_(False)

        view = WhipView.alloc().initWithFrame_(NSMakeRect(0, 0, W, H))
        win.setContentView_(view)
        win.makeKeyAndOrderFront_(None)

        animator = Animator.alloc().init()
        animator.view = view
        animator.win = win
        animator.frames = self.frames
        self._animator = animator
        animator.start()


def play(frames: list[dict]) -> None:
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(2)  # no Dock icon
    delegate = AppDelegate.alloc().init()
    delegate.frames = frames
    app.setDelegate_(delegate)
    app.run()
