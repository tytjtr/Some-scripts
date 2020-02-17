#!/bin/bash




cd /home/

if  [[ ! -n "$TR_APP_VERSION" ]] && [[ ! -n "$TR_TORRENT_DIR" ]] && [[ ! -n "$TR_TORRENT_HASH" ]] && [[ ! -n "$TR_TORRENT_ID" ]] && [[ ! -n "$TR_TORRENT_NAME" ]] ;then
    echo "²ÎÊýÈ±Ê§"
else
    python3 /home/u2_automatic_seed_backup_tr.py "-$TR_APP_VERSION-" "-$TR_TORRENT_DIR-" "-$TR_TORRENT_HASH-" "-$TR_TORRENT_ID-" "-$TR_TORRENT_NAME-"
fi
