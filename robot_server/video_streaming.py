#!/usr/bin/env python3
import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstRtspServer", "1.0")

from gi.repository import Gst, GstRtspServer, GLib

Gst.init(None)

class CameraFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        super().__init__()
        self.launch_string = (
            "( v4l2src device=/dev/video0 io-mode=2 do-timestamp=true ! "
            "video/x-raw,width=640,height=480,framerate=30/1 ! "
            "queue max-size-buffers=1 leaky=downstream ! "
            "v4l2h264enc "
            "extra-controls=\"controls,video_bitrate=2000000,h264_i_frame_period=15\" ! "
            "h264parse config-interval=1 ! "
            "rtph264pay name=pay0 pt=96 )"
        )

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

class RTSPServer:
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        self.server.set_service("8554")

        factory = CameraFactory()
        factory.set_shared(True)

        mounts = self.server.get_mount_points()
        mounts.add_factory("/test", factory)

        self.server.attach(None)
        print("? RTSP stream ready at rtsp://<robot_ip>:8554/test")

if __name__ == "__main__":
    RTSPServer()
    GLib.MainLoop().run()
