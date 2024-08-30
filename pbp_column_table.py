import pandas as pd
fields = '''
pbp_d_comb_max_enr_amt_yn, pbp_d_comb_max_enr_amt, pbp_d_out_pocket_amt_yn, pbp_d_out_pocket_amt, pbp_d_oon_max_enr_oopc_yn, pbp_d_oon_max_enr_oopc_amt, pbp_d_maxenr_oopc_type,
pbp_d_maxenr_oopc_amt,
pbp_d_ann_deduct_yn, pbp_d_ann_deduct_amt_type, pbp_a_special_need_plan_type, pbp_a_dsnp_zerodollar, pbp_a_snp_state_cvg_yn, pbp_d_ann_deduct_amt, 
pbp_d_ann_deduct_comb_type, pbp_d_comb_deduct_yn, pbp_d_comb_deduct_partb_yn, pbp_d_inn_deduct_yn, pbp_d_inn_deduct_partb_yn, pbp_d_comb_deduct_amt,
pbp_d_oon_deduct_yn, pbp_d_oon_deduct_amt, pbp_d_inn_deduct_amt, pbp_d_oon_deduct_partb_yn,
PBP_A_CONTRACT_NUMBER, c.pbp_a_plan_identifier, 
PBP_A_SEGMENT_ID as SegmentID, 
	PBP_A_PLAN_NAME,
	PBP_A_PLAN_GEOG_NAME as GeoName, 
	PBP_A_ORG_MARKETING_NAME as CarrierName, 
	pbp_a_org_name as OrganizationName,
	m.PBP_A_PLAN_TYPE as MedicalPlanType,
	pbp_a_eghp_yn, PBP_A_ORG_TYPE, mrx_benefit_type,  pbp_a_snp_pct, pbp_a_snp_cond, m.PBP_A_PLAN_TYPE,
	pbp_a_special_need_flag, pbp_a_special_need_plan_type, 
	mrx_alt_ded_amount, mrx_alt_ded_charge, 
 PBP_A_ORG_MARKETING_NAME, 
 x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, x.pbp_b1a_bendesc_yn,x.pbp_b1a_cost_vary_tiers_yn,x.pbp_b1a_cost_vary_tier_num,x.pbp_b1a_cost_vary_low_tier,x.pbp_b1a_coins_yn
,x.pbp_b1a_copay_yn,x.pbp_b1a_mc_coins_cstshr_yn_t1,x.pbp_b1a_coins_mcs_pct_t1,x.pbp_b1a_coins_mcs_int_num_t1,x.pbp_b1a_coins_mcs_pct_int1_t1,x.pbp_b1a_coins_mcs_bgnd_int1_t1,x.pbp_b1a_coins_mcs_endd_int1_t1,x.pbp_b1a_coins_mcs_pct_int2_t1
,x.pbp_b1a_coins_mcs_bgnd_int2_t1,x.pbp_b1a_coins_mcs_endd_int2_t1,x.pbp_b1a_coins_mcs_pct_int3_t1,x.pbp_b1a_coins_mcs_bgnd_int3_t1,x.pbp_b1a_coins_mcs_endd_int3_t1,x.pbp_b1a_mc_copay_cstshr_yn_t1,x.pbp_b1a_copay_mcs_amt_t1
,x.pbp_b1a_copay_mcs_int_num_t1,x.pbp_b1a_copay_mcs_amt_int1_t1,x.pbp_b1a_copay_mcs_bgnd_int1_t1,x.pbp_b1a_copay_mcs_endd_int1_t1,x.pbp_b1a_copay_mcs_amt_int2_t1,x.pbp_b1a_copay_mcs_bgnd_int2_t1,x.pbp_b1a_copay_mcs_endd_int2_t1
,x.pbp_b1a_copay_mcs_amt_int3_t1,x.pbp_b1a_copay_mcs_bgnd_int3_t1,x.pbp_b1a_copay_mcs_endd_int3_t1, x.pbp_b1a_copay_ad_intrvl_num_t1, x.pbp_b1a_copay_ad_amt_int1_t1, x.pbp_b1a_copay_ad_bgnd_int1_t1, x.pbp_b1a_copay_ad_endd_int1_t1
,x.pbp_b1a_mc_coins_cstshr_yn_t2,x.pbp_b1a_coins_mcs_pct_t2,x.pbp_b1a_coins_mcs_int_num_t2,x.pbp_b1a_coins_mcs_pct_int1_t2,x.pbp_b1a_coins_mcs_bgnd_int1_t2,x.pbp_b1a_coins_mcs_endd_int1_t2,x.pbp_b1a_coins_mcs_pct_int2_t2,x.pbp_b1a_coins_mcs_bgnd_int2_t2
,x.pbp_b1a_coins_mcs_endd_int2_t2,x.pbp_b1a_coins_mcs_pct_int3_t2,x.pbp_b1a_coins_mcs_bgnd_int3_t2,x.pbp_b1a_coins_mcs_endd_int3_t2,x.pbp_b1a_mc_copay_cstshr_yn_t2,x.pbp_b1a_copay_mcs_amt_t2,x.pbp_b1a_copay_mcs_int_num_t2
,x.pbp_b1a_copay_mcs_amt_int1_t2,x.pbp_b1a_copay_mcs_bgnd_int1_t2,x.pbp_b1a_copay_mcs_endd_int1_t2,x.pbp_b1a_copay_mcs_amt_int2_t2,x.pbp_b1a_copay_mcs_bgnd_int2_t2,x.pbp_b1a_copay_mcs_endd_int2_t2,x.pbp_b1a_copay_mcs_amt_int3_t2
,x.pbp_b1a_copay_mcs_bgnd_int3_t2,x.pbp_b1a_copay_mcs_endd_int3_t2, x.pbp_b1a_copay_ad_intrvl_num_t2, x.pbp_b1a_copay_ad_amt_int1_t2, x.pbp_b1a_copay_ad_bgnd_int1_t2, x.pbp_b1a_copay_ad_endd_int1_t2, x.pbp_b1a_ad_cost_vary_tiers_yn
,x.pbp_b1a_auth_yn ,x.pbp_b1a_refer_yn,
x.pbp_b1a_auth_yn, x.pbp_c_oon_coins_ihs_yn, x.pbp_c_oon_coins_iha_mc_cost_yn, x.pbp_c_oon_coins_iha_pct, x.pbp_c_oon_coins_iha_intrvl_num, 
    x.pbp_c_oon_coins_iha_pct_i1, x.pbp_c_oon_coins_iha_bgnd_i1, x.pbp_c_oon_coins_iha_endd_i1,
    x.pbp_c_oon_coins_iha_pct_i2, x.pbp_c_oon_coins_iha_bgnd_i2,x.pbp_c_oon_coins_iha_endd_i2,
    x.pbp_c_oon_coins_iha_pct_i3, x.pbp_c_oon_coins_iha_bgnd_i3,x.pbp_c_oon_coins_iha_endd_i3,
    x.pbp_c_oon_copay_ihs_yn,  x.pbp_c_oon_copay_iha_mc_cost_yn, x.pbp_c_oon_copay_iha_ps_amt,x.pbp_c_oon_copay_iha_intrvl_num,
    x.pbp_c_oon_copay_iha_amt_i1, x.pbp_c_oon_copay_iha_bgnd_i1, x.pbp_c_oon_copay_iha_endd_i1,
    x.pbp_c_oon_copay_iha_amt_i2, x.pbp_c_oon_copay_iha_bgnd_i2,x.pbp_c_oon_copay_iha_endd_i2,
    x.pbp_c_oon_copay_iha_amt_i3, x.pbp_c_oon_copay_iha_bgnd_i3,x.pbp_c_oon_copay_iha_endd_i3,
    x.pbp_c_pos_yn, x.pbp_c_pos_mc_bendesc_subcats,
    x.pbp_c_pos_coins_ihs_yn, x.pbp_c_pos_coins_iha_mc_cost_yn, x.pbp_c_pos_coins_iha_intrvl_num, x.pbp_c_pos_coins_iha_pct,
    x.pbp_c_pos_coins_iha_pct_i1, x.pbp_c_pos_coins_iha_bgnd_i1, x.pbp_c_pos_coins_iha_endd_i1,
    x.pbp_c_pos_coins_iha_pct_i2, x.pbp_c_pos_coins_iha_bgnd_i2,x.pbp_c_pos_coins_iha_endd_i2,
    x.pbp_c_pos_coins_iha_pct_i3, x.pbp_c_pos_coins_iha_bgnd_i3,x.pbp_c_pos_coins_iha_endd_i3,
    x.pbp_c_pos_copay_ihs_yn, x.pbp_c_pos_copay_iha_mc_cost_yn, x.pbp_c_pos_copay_iha_intrvl_num, x.pbp_c_pos_copay_iha_ps_amt,
    x.pbp_c_pos_copay_iha_amt_i1, x.pbp_c_pos_copay_iha_bgnd_i1, x.pbp_c_pos_copay_iha_endd_i1,
    x.pbp_c_pos_copay_iha_amt_i2, x.pbp_c_pos_copay_iha_bgnd_i2,x.pbp_c_pos_copay_iha_endd_i2,
    x.pbp_c_pos_copay_iha_amt_i3, x.pbp_c_pos_copay_iha_bgnd_i3,x.pbp_c_pos_copay_iha_endd_i3,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, x.pbp_b2_bendesc_yn,x.pbp_b2_cost_vary_tiers_yn,x.pbp_b2_cost_vary_tier_num,x.pbp_b2_cost_vary_low_tier,x.pbp_b2_coins_yn
,x.pbp_b2_copay_yn,x.pbp_b2_mc_coins_cstshr_yn_t1,x.pbp_b2_coins_mcs_pct_t1,x.pbp_b2_coins_mcs_int_num_t1,x.pbp_b2_coins_mcs_pct_int1_t1,x.pbp_b2_coins_mcs_bgnd_int1_t1,x.pbp_b2_coins_mcs_endd_int1_t1,x.pbp_b2_coins_mcs_pct_int2_t1
,x.pbp_b2_coins_mcs_bgnd_int2_t1,x.pbp_b2_coins_mcs_endd_int2_t1,x.pbp_b2_coins_mcs_pct_int3_t1,x.pbp_b2_coins_mcs_bgnd_int3_t1,x.pbp_b2_coins_mcs_endd_int3_t1,x.pbp_b2_mc_copay_cstshr_yn_t1,x.pbp_b2_copay_mcs_amt_t1
,x.pbp_b2_copay_mcs_int_num_t1,x.pbp_b2_copay_mcs_amt_int1_t1,x.pbp_b2_copay_mcs_bgnd_int1_t1,x.pbp_b2_copay_mcs_endd_int1_t1,x.pbp_b2_copay_mcs_amt_int2_t1,x.pbp_b2_copay_mcs_bgnd_int2_t1,x.pbp_b2_copay_mcs_endd_int2_t1
,x.pbp_b2_copay_mcs_amt_int3_t1,x.pbp_b2_copay_mcs_bgnd_int3_t1,x.pbp_b2_copay_mcs_endd_int3_t1, x.pbp_b2_copay_ad_intrvl_num_t1, x.pbp_b2_copay_ad_amt_int1_t1, x.pbp_b2_copay_ad_bgnd_int1_t1, x.pbp_b2_copay_ad_endd_int1_t1
,x.pbp_b2_mc_coins_cstshr_yn_t2,x.pbp_b2_coins_mcs_pct_t2,x.pbp_b2_coins_mcs_int_num_t2,x.pbp_b2_coins_mcs_pct_int1_t2,x.pbp_b2_coins_mcs_bgnd_int1_t2,x.pbp_b2_coins_mcs_endd_int1_t2,x.pbp_b2_coins_mcs_pct_int2_t2,x.pbp_b2_coins_mcs_bgnd_int2_t2
,x.pbp_b2_coins_mcs_endd_int2_t2,x.pbp_b2_coins_mcs_pct_int3_t2,x.pbp_b2_coins_mcs_bgnd_int3_t2,x.pbp_b2_coins_mcs_endd_int3_t2,x.pbp_b2_mc_copay_cstshr_yn_t2,x.pbp_b2_copay_mcs_amt_t2,x.pbp_b2_copay_mcs_int_num_t2
,x.pbp_b2_copay_mcs_amt_int1_t2,x.pbp_b2_copay_mcs_bgnd_int1_t2,x.pbp_b2_copay_mcs_endd_int1_t2,x.pbp_b2_copay_mcs_amt_int2_t2,x.pbp_b2_copay_mcs_bgnd_int2_t2,x.pbp_b2_copay_mcs_endd_int2_t2,x.pbp_b2_copay_mcs_amt_int3_t2
,x.pbp_b2_copay_mcs_bgnd_int3_t2,x.pbp_b2_copay_mcs_endd_int3_t2, x.pbp_b2_copay_ad_intrvl_num_t2, x.pbp_b2_copay_ad_amt_int1_t2, x.pbp_b2_copay_ad_bgnd_int1_t2, x.pbp_b2_copay_ad_endd_int1_t2, x.pbp_b2_ad_cost_vary_tiers_yn
,x.pbp_b2_auth_yn ,x.pbp_b2_refer_yn,
x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7d_copay_yn,x.pbp_b7d_copay_amt_mc_min,x.pbp_b7d_copay_amt_mc_max,
    x.pbp_b7d_coins_yn,x.pbp_b7d_coins_pct_mc_min,x.pbp_b7d_coins_pct_mc_max,
    x.pbp_c_oon_yn, 
    x.pbp_c_oon_outpt_coins_yn,x.pbp_c_oon_outpt_coins_min_pct,x.pbp_c_oon_outpt_coins_max_pct,
    x.pbp_c_oon_outpt_copay_yn,x.pbp_c_oon_outpt_copay_min_amt,x.pbp_c_oon_outpt_copay_max_amt,
    x.pbp_c_pos_outpt_coins_yn,x.pbp_c_pos_outpt_coins_min_pct,x.pbp_c_pos_outpt_coins_max_pct,
    x.pbp_c_pos_outpt_copay_yn,x.pbp_c_pos_outpt_copay_min_amt,x.pbp_c_pos_outpt_copay_max_amt,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b16a_copay_cserv_sc_pov_yn,x.pbp_b16a_coins_cserv_sc_pov_yn, 
    x.pbp_b16a_bendesc_yn, x.pbp_b16a_bendesc_ehc,
    x.pbp_b16a_coins_yn,x.pbp_b16a_bendesc_ehc,x.pbp_b16a_coins_pct_oe,x.pbp_b16a_coins_pct_maxoe, 
    x.pbp_b16a_copay_yn,x.pbp_b16a_bendesc_ehc,x.pbp_b16a_copay_amt_oemin,x.pbp_b16a_copay_amt_oemax,
    x.pbp_b16a_maxplan_yn, x.pbp_b16a_maxplan_amt,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b16a_copay_cserv_sc_pov_yn,x.pbp_b16a_coins_cserv_sc_pov_yn, 
    x.pbp_b16a_bendesc_yn, x.pbp_b16a_bendesc_ehc,
    x.pbp_b16a_coins_yn,x.pbp_b16a_bendesc_ehc,x.pbp_b16a_coins_pct_pc,x.pbp_b16a_coins_pct_maxpc, 
    x.pbp_b16a_copay_yn,x.pbp_b16a_bendesc_ehc,x.pbp_b16a_copay_amt_pcmin,x.pbp_b16a_copay_amt_pcmax,
    x.pbp_b16a_maxplan_yn, x.pbp_b16a_maxplan_amt,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b16a_copay_cserv_sc_pov_yn,x.pbp_b16a_coins_cserv_sc_pov_yn, 
    x.pbp_b16a_bendesc_yn, x.pbp_b16a_bendesc_ehc,
    x.pbp_b16a_coins_yn,x.pbp_b16a_bendesc_ehc,x.pbp_b16a_coins_pct_ft,x.pbp_b16a_coins_pct_maxft, 
    x.pbp_b16a_copay_yn,x.pbp_b16a_bendesc_ehc,x.pbp_b16a_copay_amt_ftmin,x.pbp_b16a_copay_amt_ftmax,
    x.pbp_b16a_maxplan_yn, x.pbp_b16a_maxplan_amt,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
                                            x.pbp_b8a_maxenr_yn, x.pbp_b8a_maxenr_amt,
    x.pbp_b8a_coins_yn,x.pbp_b8a_coins_ehc,x.pbp_b8a_coins_pct_dmc,x.pbp_b8a_coins_pct_dmc_max,
    x.pbp_b8a_copay_yn,x.pbp_b8a_copay_ehc,x.pbp_b8a_copay_min_dmc_amt,x.pbp_b8a_copay_max_dmc_amt,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
                                             x.pbp_b8b_maxenr_yn, x.pbp_b8b_maxenr_amt,
    x.pbp_b8b_coins_yn,x.pbp_b8b_coins_ehc,x.pbp_b8b_coins_pct_drs,x.pbp_b8b_coins_pct_drs_max,
    x.pbp_b8b_copay_yn,x.pbp_b8b_copay_ehc,x.pbp_b8b_copay_amt_drs,x.pbp_b8b_copay_amt_drs_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
                                             x.pbp_b8b_maxenr_yn, x.pbp_b8b_maxenr_amt,
    x.pbp_b8b_coins_yn,x.pbp_b8b_coins_ehc,x.pbp_b8b_coins_pct_cmc,x.pbp_b8b_coins_pct_cmc_max,
    x.pbp_b8b_copay_yn,x.pbp_b8b_copay_ehc,x.pbp_b8b_copay_mc_amt,x.pbp_b8b_copay_mc_amt_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b4a_coins_yn,x.pbp_b4a_coins_pct_mc_min,x.pbp_b4a_coins_pct_mc_max,
    x.pbp_b4a_copay_yn,x.pbp_b4a_copay_amt_mc_min,x.pbp_b4a_copay_amt_mc_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b4b_coins_yn,x.pbp_b4b_coins_pct_mc_min,x.pbp_b4b_coins_pct_mc_max,
    x.pbp_b4b_copay_yn,x.pbp_b4b_copay_amt_mc_min,x.pbp_b4b_copay_amt_mc_max,
    pbp_b14a_mc_prevent_attest,x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
                                            x.pbp_b10a_maxenr_yn, x.pbp_b10a_maxenr_gas_amt,
    x.pbp_b10a_coins_yn,x.pbp_b10a_coins_ehc,x.pbp_b10a_coins_gas_pct_min,x.pbp_b10a_coins_gas_pct_max,
    x.pbp_b10a_copay_yn,x.pbp_b10a_copay_ehc,x.pbp_b10a_copay_gas_amt_min,x.pbp_b10a_copay_gas_amt_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b7c_coins_yn,x.pbp_b7c_coins_pct_mc_min,x.pbp_b7c_coins_pct_mc_max,
    x.pbp_b7c_copay_yn,x.pbp_b7c_copay_mc_amt_min,x.pbp_b7c_copay_mc_amt_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b7i_coins_yn,x.pbp_b7i_coins_pct_mc_min,x.pbp_b7i_coins_pct_mc_max,
    x.pbp_b7i_copay_yn,x.pbp_b7i_copay_mc_amt_min,x.pbp_b7i_copay_mc_amt_max,x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
                                            x.pbp_b7e_maxenr_yn, x.pbp_b7e_maxenr_amt,
    x.pbp_b7e_coins_yn,x.pbp_b7e_coins_ehc,x.pbp_b7e_coins_mcgs_minpct,x.pbp_b7e_coins_mcgs_maxpct,
    x.pbp_b7e_copay_yn,x.pbp_b7e_copay_ehc,x.pbp_b7e_copay_mcgs_minamt,x.pbp_b7e_copay_mcgs_maxamt, x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
                                            x.pbp_b7e_maxenr_yn, x.pbp_b7e_maxenr_amt,
    x.pbp_b7e_coins_yn,x.pbp_b7e_coins_ehc,x.pbp_b7e_coins_mcis_minpct,x.pbp_b7e_coins_mcis_maxpct,
    x.pbp_b7e_copay_yn,x.pbp_b7e_copay_ehc,x.pbp_b7e_copay_mcis_minamt,x.pbp_b7e_copay_mcis_maxamt, x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
                                            x.pbp_b7h_maxenr_yn, x.pbp_b7h_maxenr_amt,
    x.pbp_b7h_coins_yn,x.pbp_b7h_coins_ehc,x.pbp_b7h_coins_mcgs_minpct,x.pbp_b7h_coins_mcgs_maxpct,
    x.pbp_b7h_copay_yn,x.pbp_b7h_copay_ehc,x.pbp_b7h_copay_mcgs_minamt,x.pbp_b7h_copay_mcgs_maxamt, x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
                                            x.pbp_b7h_maxenr_yn, x.pbp_b7h_maxenr_amt,
    x.pbp_b7h_coins_yn,x.pbp_b7h_coins_ehc,x.pbp_b7h_coins_mcis_minpct,x.pbp_b7h_coins_mcis_maxpct,
    x.pbp_b7h_copay_yn,x.pbp_b7h_copay_ehc,x.pbp_b7h_copay_mcis_minamt,x.pbp_b7h_copay_mcis_maxamt, x.pbp_a_special_need_plan_type, 
                                             x.pbp_b18a_bendesc_yn, x.pbp_b18a_bendesc_ehc,
    x.pbp_b18a_coins_yn,x.pbp_b18a_coins_ehc,x.pbp_b18a_coins_pct_rht,x.pbp_b18a_coins_pct_max_rht,
    x.pbp_b18a_copay_yn,x.pbp_b18a_copay_ehc,x.pbp_b18a_copay_amt_rht,x.pbp_b18a_copay_amt_max_rht, x.pbp_a_special_need_plan_type,
                                             x.pbp_b18a_bendesc_yn, x.pbp_b18a_bendesc_ehc,
    x.pbp_b18a_coins_yn,x.pbp_b18a_coins_ehc,x.pbp_b18a_coins_pct_fha,x.pbp_b18a_coins_pct_max_fha,
    x.pbp_b18a_copay_yn,x.pbp_b18a_copay_ehc,x.pbp_b18a_copay_amt_fha,x.pbp_b18a_copay_amt_max_fha, x.pbp_a_special_need_plan_type, 
                                             x.pbp_b18b_bendesc_yn, x.pbp_b18b_bendesc_ehc,
    x.pbp_b18b_coins_yn,x.pbp_b18b_coins_ehc,x.pbp_b18b_coins_pct_at_min,x.pbp_b18b_coins_pct_at_max,
    x.pbp_b18b_copay_yn,x.pbp_b18b_copay_ehc,x.pbp_b18b_copay_at_min_amt,x.pbp_b18b_copay_at_max_amt, x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_cl_min,x.pbp_b17b_coins_pct_cl_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_cl_min,x.pbp_b17b_copay_amt_cl_max, x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_egs_min, x.pbp_b17b_coins_pct_egs_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_egs_min, x.pbp_b17b_copay_amt_egs_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_upg_min, x.pbp_b17b_coins_pct_upg_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_upg_min, x.pbp_b17b_copay_amt_upg_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_egf_min,x.pbp_b17b_coins_pct_egf_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_egf_min, x.pbp_b17b_copay_amt_egf_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_egl_min, x.pbp_b17b_coins_pct_egl_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_egl_min, x.pbp_b17b_copay_amt_egl_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_b17a_bendesc_yn, x.pbp_b17a_bendesc_ehc,
    x.pbp_b17a_coins_yn,x.pbp_b17a_coins_ehc,x.pbp_b17a_coins_pct_rex_min, x.pbp_b17a_coins_pct_rex_max,
    x.pbp_b17a_copay_yn,x.pbp_b17a_copay_ehc,x.pbp_b17a_copay_amt_rex_min, x.pbp_b17a_copay_amt_rex_max,
    x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
x.mrx_b_coins_yn,x.mrx_b_coins_ehc,x.mrx_b_chemo_coins_min_pct,x.mrx_b_chemo_coins_max_pct,
x.mrx_b_copay_yn,x.mrx_b_copay_ehc,x.mrx_b_chemo_copay_amt_min,x.mrx_b_chemo_copay_amt_max,
x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
x.mrx_b_coins_yn,x.mrx_b_coins_ehc,x.mrx_b_coins_min_pct,x.mrx_b_coins_max_pct,
x.mrx_b_copay_yn,x.mrx_b_copay_ehc,x.mrx_b_copay_min_amt,x.mrx_b_copay_max_amt,
x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                             x.pbp_c_oon_yn,x.pbp_c_pos_yn,
x.mrx_b_ira_coins_yn,x.mrx_b_ira_coins_min_pct,x.mrx_b_ira_coins_max_pct,
x.mrx_b_ira_copay_yn,x.mrx_b_ira_copay_amt_min,x.mrx_b_ira_copay_amt_max
'''

def get_table_name(table_column):
    if table_column.startswith('pbp_a_'):
        return 'PBP'
    elif table_column.startswith('pbp_c_oon_outpt_'):
        return 'PBPC_OON'
    elif table_column.startswith('pbp_c_pos_outpt_'):
        return 'PBPC_POS'
    elif table_column.startswith('pbp_c_'):
        return 'PBPC'
    elif table_column.startswith('pbp_d_'):
        return 'PBPD'
    elif table_column.startswith('mrx_b_'):
        return 'PBPB15'
    elif table_column.startswith('mrx_'):
        return 'PBPMRX'
    elif table_column.startswith('pbp_b1a_'):
        return 'PBPB1'
    elif table_column.startswith('pbp_b2_'):
        return 'PBPB2'
    elif table_column.startswith('pbp_b4a_'):
        return 'PBPB4'
    elif table_column.startswith('pbp_b4b_'):
        return 'PBPB4'
    elif table_column.startswith('pbp_b7a_'):
        return 'PBPB7'
    elif table_column.startswith('pbp_b7c_'):
        return 'PBPB7'
    elif table_column.startswith('pbp_b7d_'):
        return 'PBPB7'
    elif table_column.startswith('pbp_b7e_'):
        return 'PBPB7'
    elif table_column.startswith('pbp_b7i_'):
        return 'PBPB7'
    elif table_column.startswith('pbp_b7h_'):
        return 'PBPB7'
    elif table_column.startswith('pbp_b8a_'):
        return 'PBPB8'
    elif table_column.startswith('pbp_b8b_'):
        return 'PBPB8'
    elif table_column.startswith('pbp_b9a_'):
        return 'PBPB9'
    elif table_column.startswith('pbp_b10a_'):
        return 'PBPB10'
    elif table_column.startswith('pbp_b14a_'):
        return 'PBPB14'
    elif table_column.startswith('pbp_b16a_'):
        return 'PBPB16'
    elif table_column.startswith('pbp_b16a_'):
        return 'PBPB16'
    elif table_column.startswith('pbp_b17a_'):
        return 'PBPB17'
    elif table_column.startswith('pbp_b17b_'):
        return 'PBPB17'
    elif table_column.startswith('pbp_b18a_'):
        return 'PBPB18'
    elif table_column.startswith('pbp_b18b_'):
        return 'PBPB18'
    else:
        raise(Exception('Undefined table: ' + table_column))
    return ''

def clean_column_names(table_column):
    table_column = table_column.lower()
    if ' as ' in table_column:
        table_column = table_column.split(' as ')[0]
    if '.' in table_column:
        table_column = table_column.split('.')[1]
    return table_column.strip()
    
        
fields = fields.split(',')
df_columns = pd.DataFrame({'table_column': fields})
df_columns['table_column'] = df_columns.apply(lambda x: clean_column_names(x.table_column), axis=1)
df_columns.drop_duplicates(inplace=True)
df_columns['table_name'] = df_columns.apply(lambda x: get_table_name(x.table_column), axis=1)
df_columns.to_csv('PBP_Table_Column.csv', index=False)
