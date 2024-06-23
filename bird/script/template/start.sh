#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: %s

export service_file=%s
export bin_dir=%s
export svrd=%s
export log_conf=%s
export proc_key=%s
export game_id=%s
export log_file=%s
export ext_param='%s'

source ${bin_dir}/script/template/base.sh

log "cd ${bin_dir}"
cd ${bin_dir}

log  "./${svrd} ${log_conf} ${proc_key} ${game_id} '${ext_param}'"
./${svrd} ${log_conf} ${proc_key} ${game_id} "${ext_param}" >> ${log_file} 2>&1
