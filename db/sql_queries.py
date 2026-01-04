ADD_NEW_CUSTOMER_QUERY = """
            INSERT INTO customers (ssn, fname, lname, birth_date, sex, tel_home, tel_mobile, address, town, postal_code, status, org, occupation, hobbies, referer, glasses_num, lenses_num, mailing, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

ADD_GLASSES_TEST_QUERY = """            INSERT INTO glasses_tests (
                customer_id, exam_date, examiner,
                r_fv, r_sphere, r_cylinder, r_axis, r_prism, r_base, r_va, both_va, r_add_read, r_add_int, r_add_bif, r_add_mul, r_high, r_pd, sum_pd, near_pd,
                l_fv, l_sphere, l_cylinder, l_axis, l_prism, l_base, l_va, l_add_read, l_add_int, l_add_bif, l_add_mul, l_high, l_pd,
                dominant_eye, r_iop, l_iop, glasses_role, lenses_material, lenses_diameter_1, lenses_diameter_2, lenses_diameter_decentration_horizontal, lenses_diameter_decentration_vertical, segment_diameter, lenses_manufacturer, lenses_color, lenses_coated, catalog_num, frame_manufacturer, frame_supplier, frame_model, frame_size, frame_bar_length, frame_color,
                diagnosis, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

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
                r_fv=?, r_sphere=?, r_cylinder=?, r_axis=?, r_prism=?, r_base=?, r_va=?, both_va=?, r_add_read=?, r_add_int=?, r_add_bif=?, r_add_mul=?, r_high=?, r_pd=?, sum_pd=?, near_pd=?,
                l_fv=?, l_sphere=?, l_cylinder=?, l_axis=?, l_prism=?, l_base=?, l_va=?, l_add_read=?, l_add_int=?, l_add_bif=?, l_add_mul=?, l_high=?, l_pd=?,
                dominant_eye=?, r_iop=?, l_iop=?, glasses_role=?, lenses_material=?, lenses_diameter_1=?, lenses_diameter_2=?, lenses_diameter_decentration_horizontal=?, lenses_diameter_decentration_vertical=?, segment_diameter=?, lenses_manufacturer=?, lenses_color=?, lenses_coated=?, catalog_num=?, frame_manufacturer=?, frame_supplier=?, frame_model=?, frame_size=?, frame_bar_length=?, frame_color=?,
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


