#!/usr/bin/env python
# License: GPLv3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>

from typing import TYPE_CHECKING, Optional

from .base import (
    MATCH_TAB_OPTION,
    MATCH_WINDOW_OPTION,
    ArgsType,
    Boss,
    PayloadGetType,
    PayloadType,
    RCOptions,
    RemoteCommand,
    ResponseType,
    Window,
)

if TYPE_CHECKING:
    from kitty.cli_stub import SendKeyRCOptions as CLIOptions


class SendKey(RemoteCommand):
    protocol_spec = __doc__ = '''
    keys+/list.str: The keys to send
    match/str: A string indicating the window to send text to
    match_tab/str: A string indicating the tab to send text to
    all/bool: A boolean indicating all windows should be matched.
    exclude_active/bool: A boolean that prevents sending text to the active window
    '''
    short_desc = 'Send arbitrary key presses to the specified windows'
    desc = (
        'Send arbitrary key presses to specified windows. All specified keys are sent first as press events'
        ' then as release events in reverse order. Keys are sent to the programs running in the windows.'
        ' They are sent only if the current keyboard mode for the program supports the particular key.'
        ' For example: send-key ctrl+a ctrl+b'
    )
    options_spec = MATCH_WINDOW_OPTION + '\n\n' + MATCH_TAB_OPTION.replace('--match -m', '--match-tab -t') + '''\n
--all
type=bool-set
Match all windows.


--exclude-active
type=bool-set
Do not send text to the active window, even if it is one of the matched windows.
'''
    args = RemoteCommand.Args(spec='[KEYS TO SEND ...]', json_field='keys')

    def message_to_kitty(self, global_opts: RCOptions, opts: 'CLIOptions', args: ArgsType) -> PayloadType:
        ret = {'match': opts.match, 'keys': args, 'match_tab': opts.match_tab, 'all': opts.all, 'exclude_active': opts.exclude_active}
        return ret

    def response_from_kitty(self, boss: Boss, window: Optional[Window], payload_get: PayloadGetType) -> ResponseType:
        windows = self.windows_for_payload(boss, None, payload_get)
        keys = payload_get('keys')
        sent = False
        for w in windows:
            if not w.send_key(*keys):
                sent = True
        sent
        return None


send_key = SendKey()
