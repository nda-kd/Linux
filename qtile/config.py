# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from typing import List  #noqa: F401

##### DEFINING SOME VARIABLES #####
mod = "mod4"                                       # Sets mod key to SUPER/WINDOWS
myTerm = "termite"                                 # My terminal of choice
myConfig = "/home/neda/.config/qtile/config.py"    # The Qtile config file location

##### KEYBINDINGS #####
keys = [

    ### The essentials
    Key([mod], "z", lazy.spawn("chromium")),
    Key([mod], "x", lazy.spawn("code")),
    Key([mod], "c", lazy.spawn("firefox")),
    Key([mod], "v", lazy.spawn("vlc")),
    Key([mod], "s", lazy.spawn("pcmanfm")),
    Key([mod], "d", lazy.spawn("dmenu_run -p 'Run: '" )),
    Key([mod], "Return",lazy.spawn(myTerm)),

   
    ### Window controls
    
   Key( [mod], "k",
        lazy.layout.down(),
        desc='Move focus down in current stack pane'),

   Key([mod], "j",
        lazy.layout.up(),
        desc='Move focus up in current stack pane'),

    Key([mod, "control"], "k",
        lazy.layout.shuffle_down(),
        desc='Move windows down in current stack'),

    Key([mod, "control"], "j",
        lazy.layout.shuffle_up(),
        desc='Move windows up in current stack'),

    Key([mod], "h",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'),

    Key([mod], "l",
         lazy.layout.shrink(),
         lazy.layout.decrease_nmaster(),
         desc='Shrink window (MonadTall), decrease number in master pane (Tile)'),

    Key([mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'),

    Key([mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'),

    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'),

    ### Stack controls
    Key([mod], "space",
        lazy.layout.next(),
        desc='Switch window focus to other pane(s) of stack'),

    Key([mod, "shift"], "space",
        lazy.layout.rotate(),
        desc='Switch which side main pane occupies (XmonadTall)'),

    Key([mod, "control"], "Return",
        lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'),

    Key([mod], "Tab",
        lazy.next_layout(), 
        desc='Toggle through layouts'),

    #power
    Key([mod], "a",
        lazy.window.kill(),
        desc='Kill active window'),

    Key([mod, "control"], "r",
        lazy.restart(),
        desc='Restart Qtile'),

    Key([mod, "control"], "q",
        lazy.shutdown(),
        desc='Shutdown Qtile'),

]

##### GROUPS #####
group_names = [("Index", {'layout': 'stack'}),
               ("Dev", {'layout': 'max'}),
               ("Firefox", {'layout': 'max'}),
               ("Chromium", {'layout': 'max'}),
               ("Doc", {'layout': 'stack'}),
               ("SYS", {'layout': 'max'}),
               ("...", {'layout': 'max'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another gr>
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window >

##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 0.3,
                "margin": 6,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

##### THE LAYOUTS #####
layouts = [
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    #layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
     layout.Tile(shift_windows=True, **layout_theme),
     layout.TreeTab(fontsize = 10,
         sections = ["FIRST", "SECOND"],
         section_fontsize = 7,
         bg_color = "141414",
         active_bg = "90C435",
         active_fg = "000000",
         inactive_bg = "384323",
         inactive_fg = "a0a0a0",
         padding_y = 5,
         section_top = 10,
         panel_width = 200),

     layout.Floating(**layout_theme),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

##### COLORS #####
colors = [["#100f21", "#100f21"], # panel background
          ["#1f93db", "#1f93db"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#2694ed", "#2694ed"], # border line color for current tab
          ["#8d62a9", "#8d62a9"], # border line color for other tab and odd widgets
          ["#668bd7", "#668bd7"], # color for the even widgets
          ["#9ed2f7", "#9ed2f7"]] # texbxes


widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
    background=colors[0]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper='~/Downloads/Image/wallpaper4k.jpg',
        wallpaper_mode='stretch',
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
                        custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                        padding = 0,
                        scale=0.7
                        ),

                widget.GroupBox(
                       fontsize = 13,
                        margin_y = 3,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 2,
                        active = colors[2],
                        inactive = "#5c5b78",
                        rounded = False,
                        highlight_color = colors[0],
                        highlight_method = "line",
                        this_current_screen_border = colors[3],
                        this_screen_border = colors [4],
                        other_current_screen_border = colors[0],
                        other_screen_border = colors[0],
                        foreground = colors[2]),

                widget.TextBox("| ", name="default"),
              # widget.Prompt(),
                widget.WindowName(),
              #  widget.TextBox("|", name="default"),
              #  widget.QuickExit(),
                widget.Systray(),

                widget.TextBox("| Net:", name="default",
                    foreground=colors[6],fontsize= 14),

                widget.Net(
                        interface = "wlp2s0",
                        format = '{down} ↓↑{up}'),

                widget.TextBox("| CPU:", name="default",
                    foreground=colors[6],fontsize=14),

                widget.CPUGraph(line_width=2,
                    type="line",
                    background="#111111"),

                widget.TextBox("| Mem:", name="default",
                    foreground=colors[6],fontsize=14),

                widget.MemoryGraph(),

                widget.TextBox("| volume: ", name="default",
                    foreground=colors[6],fontsize=14),

                widget.Volume(),

                widget.Clock(format="%A, %B %d  [ %H:%M:%S ]",
                        background=colors[6],foreground=colors[0],fontsize=12
                    ),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

##### STARTUP APPLICATIONS #####
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])



# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
