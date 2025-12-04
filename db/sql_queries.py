ADD_GLASSES_TEST_QUERY = """            INSERT INTO glasses_tests (
                customer_id, exam_date, examiner,
                r_fv_numerator, r_fv_denominator,
                r_sphere, r_cylinder, r_axis, r_prism, r_base, r_va, r_add_read, r_add_int, r_add_bif, r_add_mul, r_high,
                l_fv_numerator, l_fv_denominator, l_sphere, l_cylinder, l_axis, l_prism, l_base, l_va, l_add_read, l_add_int, l_add_bif, l_add_mul, l_high,
                pupil_distance, dominant_eye, iop, glasses_role, lenses_material, lenses_diameter, segment_diameter, lenses_manufacturer, lenses_color, catalog_num, frame_manufacturer, frame_supplier, frame_model, frame_size, frame_bar_length, frame_color,
                diagnosis, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

orig_ADD_GLASSES_TEST_QUERY = """ 
            INSERT INTO glasses_tests (
                customer_id, exam_date, examiner,
                r_sphere, r_cylinder, r_axis, r_add, r_va,
                l_sphere, l_cylinder, l_axis, l_add, l_va,
                pupil_distance, diagnosis, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

UPDATE_GLASSES_TEST_QUERY = """
            UPDATE glasses_tests
            SET customer_id=?, exam_date=?, examiner=?,
                r_fv_numerator=?, r_fv_denominator=?,
                r_sphere=?, r_cylinder=?, r_axis=?, r_prism=?, r_base=?, r_va=?, r_add_read=?, r_add_int=?, r_add_bif=?, r_add_mul=?, r_high=?,
                l_fv_numerator=?, l_fv_denominator=?, l_sphere=?, l_cylinder=?, l_axis=?, l_prism=?, l_base=?, l_va=?, l_add_read=?, l_add_int=?, l_add_bif=?, l_add_mul=?, l_high=?,
                pupil_distance=?, dominant_eye=?, iop=?, glasses_role=?, lenses_material=?, lenses_diameter=?, segment_diameter=?, lenses_manufacturer=?, lenses_color=?, catalog_num=?, frame_manufacturer=?, frame_supplier=?, frame_model=?, frame_size=?, frame_bar_length=?, frame_color=?,
                diagnosis=?, notes=?
            WHERE id=?
        """

orig_UPDATE_GLASSES_TEST_QUERY = """
            UPDATE glasses_tests
            SET customer_id=?, exam_date=?, examiner=?,
                r_sphere=?, r_cylinder=?, r_axis=?, r_add=?, r_va=?,
                l_sphere=?, l_cylinder=?, l_axis=?, l_add=?, l_va=?,
                pupil_distance=?, diagnosis=?, notes=?
            WHERE id=?
        """


