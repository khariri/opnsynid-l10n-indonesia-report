# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from openerp.report import report_sxw 


class Parser(report_sxw.rml_parse):

	def __init__(self, cr, uid, name, context):
		super(Parser, self).__init__(cr, uid, name, context)
		self.list_config = []
		self.localcontext.update({
			"time": time,
			"get_data": self._get_data,
		})

	def set_context(self, objects, data, ids, report_type=None):
		self.form = data["form"]
		self.date_start = self.form["date_start"]
		self.date_end = self.form["date_end"]
		self.warehouse_ids = self.form["warehouse_ids"]
		return super(Parser, self).set_context(objects, data, ids, report_type)

	def _get_data(self):
		data = []
		obj_data = self.pool.get(
			"l10n_id.djbc_kb_lap_posisi_wip")
		no = 1

		criteria = [
			("tgl_penerimaan", ">=", self.date_start),
			("tgl_penerimaan", "<=", self.date_end),
			("warehouse_id", "in", self.warehouse_ids)
		]

		data_ids = obj_data.search(self.cr, self.uid, criteria)

		if data_ids:
			for data_id in obj_data.browse(self.cr, self.uid, data_ids):
				res = {
					"no": no,
					"tgl_peneriamaan": data_id.tgl_penerimaan,
					"kode_barang": data_id.kode_barang,
					"nama_barang": data_id.nama_barang,
					"satuan": data_id.satuan,
					"jumlah": data_id.jumlah,
					"warehouse_id": data_id.warehouse_id
				}
				data.append(res)
				no += 1

		return data
