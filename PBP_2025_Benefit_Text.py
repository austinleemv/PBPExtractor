'''
Module to convert PBP data to cost share text
'''
import numpy as np

class PlanYearBase():
    PLAN_YEAR = 2024
    RX_CATASTROHPIC_LIMIT = 8000
    RX_INITIAL_COVERAGE_LIMIT = 5030
    DEDAULT_RX_DEDUCTIBLE = 545
    MEDICARE_DEDUCTIBLE_PART_A = 1632
    MEDICARE_DEDUCTIBLE_PART_B = 240
    
    # utility methods
    def convert_to_currency(self, float_field):
        return '${:,.2f}'.format(float_field)
    
    def convert_to_currency_no_decimal(self, float_field):
        return '${:,.0f}'.format(float_field)
    
    def convert_to_int(self, field, null_value):
        if field is None:
            return null_value
        return int(field)

class Plan(PlanYearBase):
    def get_moop(self, pbp_d_comb_max_enr_amt_yn, pbp_d_comb_max_enr_amt, pbp_d_out_pocket_amt_yn, pbp_d_out_pocket_amt, pbp_d_oon_max_enr_oopc_yn, pbp_d_oon_max_enr_oopc_amt, pbp_d_maxenr_oopc_amt):
        #handle nan to 0
        if np.isnan(pbp_d_comb_max_enr_amt_yn):
            pbp_d_comb_max_enr_amt_yn = 0
        if np.isnan(pbp_d_out_pocket_amt_yn):
            pbp_d_out_pocket_amt_yn = 0
        if np.isnan(pbp_d_oon_max_enr_oopc_yn):
            pbp_d_oon_max_enr_oopc_yn = 0
            
        moop_text = ''
        if pbp_d_comb_max_enr_amt_yn + pbp_d_out_pocket_amt_yn + pbp_d_oon_max_enr_oopc_yn > 0:
            if pbp_d_comb_max_enr_amt_yn == 1:
                moop_text +=  f'{self.convert_to_currency_no_decimal(pbp_d_comb_max_enr_amt)} In and Out-of-network'
                if pbp_d_out_pocket_amt_yn +  pbp_d_oon_max_enr_oopc_yn > 0:
                    moop_text += '<br/>'
            if pbp_d_out_pocket_amt_yn == 1:
                moop_text += f'{self.convert_to_currency_no_decimal(pbp_d_out_pocket_amt)} In-network'
                if pbp_d_oon_max_enr_oopc_yn > 0:
                    moop_text += '<br/>'
            if pbp_d_oon_max_enr_oopc_yn == 1:
                moop_text += f'{self.convert_to_currency_no_decimal(pbp_d_oon_max_enr_oopc_amt)} Out-of-network'
            return moop_text
        else:
            if not np.isnan(pbp_d_maxenr_oopc_amt):
                return self.convert_to_currency_no_decimal(pbp_d_maxenr_oopc_amt)
            return 'Not Applicable'
        
    def get_rx_deductible_limit(self, mrx_alt_ded_amount, mrx_alt_ded_charge):
        if not np.isnan(mrx_alt_ded_amount):
            return mrx_alt_ded_amount
        if not np.isnan(mrx_alt_ded_charge):
            if int(mrx_alt_ded_charge) == 1:
                return float(self.DEDAULT_RX_DEDUCTIBLE)
        return float(0)

    def get_health_deductible_limit(self, pbp_a_special_need_plan_type, pbp_a_dsnp_zerodollar, pbp_a_snp_state_cvg_yn, 
								pbp_d_ann_deduct_yn, pbp_d_ann_deduct_amt_type, pbp_d_ann_deduct_amt, pbp_d_ann_deduct_comb_type, 
								pbp_d_comb_deduct_yn, pbp_d_comb_deduct_partb_yn, pbp_d_comb_deduct_amt,
								pbp_d_inn_deduct_yn, pbp_d_inn_deduct_partb_yn, pbp_d_inn_deduct_amt, 
                                pbp_d_oon_deduct_yn, pbp_d_oon_deduct_partb_yn, pbp_d_oon_deduct_amt):    
        if pbp_a_special_need_plan_type == 3 and pbp_a_dsnp_zerodollar == 1:
            return '$0'
        if pbp_a_special_need_plan_type == 3 and  pbp_a_snp_state_cvg_yn == 1: 
            return '$0'
        if pbp_d_ann_deduct_yn == 1:
            if pbp_d_ann_deduct_amt_type == 1:
                return f'{self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_A)} per year for some in-network and out-of-network services'
            elif pbp_d_ann_deduct_amt_type == 2:
                if pbp_a_special_need_plan_type == 3:
                    return '$0 or $240 per year for some in-network and out-of-network services.'
                return '$240 per year for some in-network and out-of-network services.'
            elif pbp_d_ann_deduct_amt_type == 4:
                return self.convert_to_currency_no_decimal(pbp_d_ann_deduct_amt) + ' annual deductible'
            else:
                if pbp_d_ann_deduct_comb_type == 1:
                    return 'Single Deductible'
                else:
                    if pbp_a_special_need_plan_type == 3:
                        return f'$0 or {self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_A)} per year for inpatient hospital services and $0 or {self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_B)} for outpatient services with a total plan deductible of $0 or $1,872 per year from in-network and out-of-network providers.'
                    else:
                        return f'{self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_A)} per year for inpatient hospital services and {self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_B)} for outpatient services with a total plan deductible of $1,872 per year from in-network and out-of-network providers.'
        elif pbp_d_comb_deduct_yn == 1:
            if pbp_d_comb_deduct_partb_yn == 1:
                if pbp_a_special_need_plan_type == 3:
                    return f'$0 or {self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_B)} per year for some in-network and out-of-network services.'
                return f'{self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_B)}  per year for some in-network and out-of-network services.'
            else:
                if pbp_a_special_need_plan_type == 3:
                    return '$0 per year in-network and out-of-network services.'
                else:
                    return self.convert_to_currency_no_decimal(pbp_d_comb_deduct_amt) + ' in and out-of-network'
        elif pbp_d_inn_deduct_yn == 1:
            if pbp_d_inn_deduct_partb_yn == 1:
                if pbp_a_special_need_plan_type == 3: 
                    if pbp_d_oon_deduct_yn == 1 and pbp_d_oon_deduct_partb_yn == 2:
                        return f'$0 or {self.convert_to_currency_no_decimal(pbp_d_oon_deduct_amt)} Out-of-network'
                    else: 
                        return f'$0 or {self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_B)}  per year for in-network services'
                else:
                    return f'{self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_B)}  per year for in-network services'
            else:
                if pbp_a_special_need_plan_type == 3:
                    return '$0'
                return f'{self.convert_to_currency_no_decimal(pbp_d_inn_deduct_amt)} In-network'
        elif pbp_d_oon_deduct_yn == 1:
            if pbp_d_oon_deduct_partb_yn == 1:
                if pbp_a_special_need_plan_type == 3:
                    return f'$0 or {self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_B)}  per year out-of-network services'
                return f'{self.convert_to_currency_no_decimal(self.MEDICARE_DEDUCTIBLE_PART_B)}  per year out-of-network services'
            else:
                if pbp_a_special_need_plan_type == 3:
                    return '$0'
                return f'{self.convert_to_currency_no_decimal(pbp_d_oon_deduct_amt)} Out-of-network'
        return '$0'
        
    def get_plan_type(self, pbp_a_eghp_yn, pbp_a_org_type, pbp_a_plan_type, mrx_benefit_type):
        '''
        Source: HPSM..usp_loadCarriersPUF_2023
        '''
        pbp_a_eghp_yn = int(pbp_a_eghp_yn)
        pbp_a_org_type = int(pbp_a_org_type)
        pbp_a_plan_type = int(pbp_a_plan_type)
        mrx_drug_ben_yn = 0
        if mrx_benefit_type in [1,2,3,4]:
            mrx_drug_ben_yn = 1
        if mrx_drug_ben_yn == 1:
            if pbp_a_org_type == 10 or pbp_a_plan_type == 29:
                return 'PDP'
            return 'MAPD'
        return 'MA'
        
    def get_snp_type(self, pbp_a_special_need_flag, pbp_a_special_need_plan_type):
        pbp_a_special_need_flag = int(pbp_a_special_need_flag)
        if pbp_a_special_need_flag == 1:
            pbp_a_special_need_plan_type = int(pbp_a_special_need_plan_type)
            if pbp_a_special_need_plan_type == 1: #	Institutional
                return 'I-SNP'
            if pbp_a_special_need_plan_type == 3: #	Dual-Eligible
                return 'D-SNP'
            if pbp_a_special_need_plan_type == 4: #	Chronic or Disabling Condition
                return 'C-SNP'
        return ''
        
    def get_qid_from_bid_id(bid_id):
        bid_id_splited = bid_id.split('_')
        bid_id_splited[1] = ('00' + bid_id_splited[1])[-3:]
        bid_id_splited[2] = ('00' + bid_id_splited[2])[-3:]
        return ''.join(bid_id_splited)

    def get_qid(self, ContractID, PlanID, SegmentID):
        return ContractID + ('000' + str(PlanID))[-3:] + ('000' + str(SegmentID))[-3:]

    @staticmethod
    def get_DrugDeductibleLimit(x):
        return Plan().get_rx_deductible_limit(x.mrx_alt_ded_amount, x.mrx_alt_ded_charge)
    @staticmethod
    def get_PlanType(x):
        return Plan().get_plan_type(x.pbp_a_eghp_yn, x.pbp_a_org_type, x.pbp_a_plan_type, x.mrx_benefit_type)
    @staticmethod
    def get_SNPType(x):
        return Plan().get_snp_type(x.pbp_a_special_need_flag, x.pbp_a_special_need_plan_type)
    @staticmethod
    def get_QID(x):
        return Plan().get_qid(x.ContractID, x.PlanID, x.SegmentID)
    @staticmethod
    def get_HealthDeductibleLimit_Text(x):
        return Plan().get_health_deductible_limit(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
								x.pbp_d_ann_deduct_yn, x.pbp_d_ann_deduct_amt_type, x.pbp_d_ann_deduct_amt, x.pbp_d_ann_deduct_comb_type, 
								x.pbp_d_comb_deduct_yn, x.pbp_d_comb_deduct_partb_yn, x.pbp_d_comb_deduct_amt,
								x.pbp_d_inn_deduct_yn, x.pbp_d_inn_deduct_partb_yn, x.pbp_d_inn_deduct_amt, 
                                x.pbp_d_oon_deduct_yn, x.pbp_d_oon_deduct_partb_yn, x.pbp_d_oon_deduct_amt)
    @staticmethod
    def get_MOOP_Text(x):
        return Plan().get_moop(x.pbp_d_comb_max_enr_amt_yn, x.pbp_d_comb_max_enr_amt, x.pbp_d_out_pocket_amt_yn, x.pbp_d_out_pocket_amt, x.pbp_d_oon_max_enr_oopc_yn, x.pbp_d_oon_max_enr_oopc_amt, x.pbp_d_maxenr_oopc_amt)
    
class Benefit(PlanYearBase):
    def has_benefits_in(self, pbp_bendesc_subcats, benefit_code):
        return ';'+ benefit_code.strip() + ';' in ';' + pbp_bendesc_subcats.strip()
     
    def is_there_a_copayment_for_service(self, ehc, digits, target_digit):
        if np.isnan(digits):
            return 1
        if np.isnan(ehc):
            return 2
        ehc = str(int(ehc))
        if len(ehc) < digits - target_digit + 1:
            return 2
        full_digits_ehc = str(int(ehc)).zfill(digits)
        if int(full_digits_ehc[target_digit - 1]) == 1:
            return 1
        return 2
    
    def get_periodicity_text(self, periodicity):
        if periodicity == 1:
            return 'Every 3 years'
        elif periodicity == 2:
            return 'Every 2 years'
        elif periodicity == 3:
            return 'Every year'
        elif periodicity == 4:
            return 'Every 6 months'
        elif periodicity == 5:
            return 'Every 3 months'
        elif periodicity == 6:
            return 'Other'
        elif periodicity == 7:
            return 'Every month'
        return ''


# Benefit Structure Type
# contains INN & ONN text generation logic
class Benefit_MC_Tiers(Benefit):
    ORIGINAL_MEDICARE_COST = 'In 2024 the amounts for each benefit period are:<br />$1,632 deductible for days 1 through 60<br />$408 copay per day for days 61 through 90'
    ORIGINAL_MEDICARE_COST_DSNP = 'In 2024 the amounts for each benefit period are $0 or:<br />$1,632 deductible for days 1 through 60<br />$408 copay per day for days 61 through 90'

    def get_1a_tier_num_coinsurance(self, pbp_a_special_need_plan_type, pbp_b1a_coins_mcs_pct_int2_t1, pbp_b1a_coins_mcs_bgnd_int2_t1,pbp_b1a_coins_mcs_endd_int2_t1):
        tier_coinsurance = ''
        if pbp_a_special_need_plan_type == 3:
            tier_coinsurance = f'0% or '
        tier_coinsurance = tier_coinsurance + f'{int(pbp_b1a_coins_mcs_pct_int2_t1)}% per day for days {int(pbp_b1a_coins_mcs_bgnd_int2_t1)} '
        if pbp_b1a_coins_mcs_endd_int2_t1 == 999:
            tier_coinsurance += 'and beyond'
        else:
            tier_coinsurance += f'through {int(pbp_b1a_coins_mcs_endd_int2_t1)}'
        return tier_coinsurance
        

    def get_1a_tier_coinsurance(self, pbp_a_special_need_plan_type, pbp_b1a_coins_mcs_int_num_t1, pbp_b1a_coins_mcs_pct_int1_t1, pbp_b1a_coins_mcs_bgnd_int1_t1,pbp_b1a_coins_mcs_endd_int1_t1,
                            pbp_b1a_coins_mcs_pct_int2_t1, pbp_b1a_coins_mcs_bgnd_int2_t1,pbp_b1a_coins_mcs_endd_int2_t1,
                            pbp_b1a_coins_mcs_pct_int3_t1, pbp_b1a_coins_mcs_bgnd_int3_t1,pbp_b1a_coins_mcs_endd_int3_t1):
        tier_copay = ''
        if pbp_b1a_coins_mcs_int_num_t1 == 1:
            if np.isnan(pbp_b1a_coins_mcs_pct_int1_t1):
                return '$0 copay'
            return f'{int(pbp_b1a_coins_mcs_pct_int1_t1)}% per stay'
        if pbp_b1a_coins_mcs_int_num_t1 > 1:
            tier_copay +=  self.get_1a_tier_num_coinsurance(pbp_a_special_need_plan_type, pbp_b1a_coins_mcs_pct_int1_t1, pbp_b1a_coins_mcs_bgnd_int1_t1,pbp_b1a_coins_mcs_endd_int1_t1)
            if pbp_b1a_coins_mcs_int_num_t1 > 2:
                tier_copay +=  '<br/>' +  self.get_1a_tier_num_coinsurance(pbp_a_special_need_plan_type, pbp_b1a_coins_mcs_pct_int2_t1, pbp_b1a_coins_mcs_bgnd_int2_t1,pbp_b1a_coins_mcs_endd_int2_t1)
                if pbp_b1a_coins_mcs_int_num_t1 > 3:
                    tier_copay += '<br/>' +  self.get_1a_tier_num_coinsurance(pbp_a_special_need_plan_type, pbp_b1a_coins_mcs_pct_int3_t1, pbp_b1a_coins_mcs_bgnd_int3_t1,pbp_b1a_coins_mcs_endd_int3_t1)
        return tier_copay


    def get_1a_tier_num_copay(self, pbp_a_special_need_plan_type, pbp_b1a_copay_mcs_amt_int1_t1, pbp_b1a_copay_mcs_bgnd_int1_t1,pbp_b1a_copay_mcs_endd_int1_t1):
        if pbp_b1a_copay_mcs_amt_int1_t1 == float(int(pbp_b1a_copay_mcs_amt_int1_t1)):
            tier_num_copay = f'{self.convert_to_currency_no_decimal(pbp_b1a_copay_mcs_amt_int1_t1)} per day for days {int(pbp_b1a_copay_mcs_bgnd_int1_t1)} '
        else:
            tier_num_copay = f'{self.convert_to_currency(pbp_b1a_copay_mcs_amt_int1_t1)} per day for days {int(pbp_b1a_copay_mcs_bgnd_int1_t1)} '
            
        if pbp_a_special_need_plan_type == 3 and pbp_b1a_copay_mcs_amt_int1_t1 > 0:
            tier_num_copay = '$0 or ' + tier_num_copay
        if pbp_b1a_copay_mcs_endd_int1_t1 == 999:
            tier_num_copay += 'and beyond'
        else:
            tier_num_copay += f'through {int(pbp_b1a_copay_mcs_endd_int1_t1)}'
        return tier_num_copay

    def get_1a_tier_copay(self, pbp_a_special_need_plan_type, pbp_b1a_copay_mcs_amt_t1,
                    pbp_b1a_copay_mcs_int_num_t1, pbp_b1a_copay_mcs_amt_int1_t1, pbp_b1a_copay_mcs_bgnd_int1_t1,pbp_b1a_copay_mcs_endd_int1_t1,
                            pbp_b1a_copay_mcs_amt_int2_t1, pbp_b1a_copay_mcs_bgnd_int2_t1,pbp_b1a_copay_mcs_endd_int2_t1,
                            pbp_b1a_copay_mcs_amt_int3_t1, pbp_b1a_copay_mcs_bgnd_int3_t1,pbp_b1a_copay_mcs_endd_int3_t1,
                            pbp_b1a_copay_ad_intrvl_num_t1, pbp_b1a_copay_ad_amt_int1_t1, pbp_b1a_copay_ad_bgnd_int1_t1, pbp_b1a_copay_ad_endd_int1_t1):
        tier_copay = ''
        if pbp_b1a_copay_mcs_amt_t1 > 0:
            tier_copay = f'{self.convert_to_currency_no_decimal(pbp_b1a_copay_mcs_amt_t1)} per stay'
            if pbp_a_special_need_plan_type == 3 and pbp_b1a_copay_mcs_amt_t1 > 0:
                tier_copay = '$0 or ' + tier_copay
        elif pbp_b1a_copay_mcs_int_num_t1 == 1:
            tier_copay = '$0 copay per stay'
        if pbp_b1a_copay_mcs_int_num_t1 > 1:
            if len(tier_copay) > 0:
                tier_copay += '<br/>'
            tier_copay += self.get_1a_tier_num_copay(pbp_a_special_need_plan_type, pbp_b1a_copay_mcs_amt_int1_t1,pbp_b1a_copay_mcs_bgnd_int1_t1,pbp_b1a_copay_mcs_endd_int1_t1)
        if pbp_b1a_copay_mcs_int_num_t1 > 2:
            tier_copay +='<br/>' 
            tier_copay += self.get_1a_tier_num_copay(pbp_a_special_need_plan_type, pbp_b1a_copay_mcs_amt_int2_t1,pbp_b1a_copay_mcs_bgnd_int2_t1,pbp_b1a_copay_mcs_endd_int2_t1)
        if pbp_b1a_copay_mcs_int_num_t1 > 3:
            tier_copay += '<br/>'
            tier_copay +=  self.get_1a_tier_num_copay(pbp_a_special_need_plan_type, pbp_b1a_copay_mcs_amt_int3_t1,pbp_b1a_copay_mcs_bgnd_int3_t1,pbp_b1a_copay_mcs_endd_int3_t1)
        if pbp_b1a_copay_ad_intrvl_num_t1 == 2:
            tier_copay += '<br/>'
            tier_copay += self.get_1a_tier_num_copay(pbp_a_special_need_plan_type, pbp_b1a_copay_ad_amt_int1_t1,pbp_b1a_copay_ad_bgnd_int1_t1,pbp_b1a_copay_ad_endd_int1_t1)
        return tier_copay

    def get_1a_inn_tier_benefit(self, pbp_a_special_need_plan_type, pbp_a_dsnp_zerodollar, pbp_a_snp_state_cvg_yn, 
                                pbp_b1a_coins_yn, pbp_b1a_mc_coins_cstshr_yn_t1, 
                                pbp_b1a_coins_mcs_int_num_t1, pbp_b1a_coins_mcs_pct_int1_t1, pbp_b1a_coins_mcs_bgnd_int1_t1,pbp_b1a_coins_mcs_endd_int1_t1,
                                pbp_b1a_coins_mcs_pct_int2_t1, pbp_b1a_coins_mcs_bgnd_int2_t1,pbp_b1a_coins_mcs_endd_int2_t1,
                                pbp_b1a_coins_mcs_pct_int3_t1, pbp_b1a_coins_mcs_bgnd_int3_t1,pbp_b1a_coins_mcs_endd_int3_t,
                                pbp_b1a_copay_yn, pbp_b1a_copay_mcs_amt_t1, pbp_b1a_mc_copay_cstshr_yn_t1, 
                                pbp_b1a_copay_mcs_int_num_t1, pbp_b1a_copay_mcs_amt_int1_t1, pbp_b1a_copay_mcs_bgnd_int1_t1,pbp_b1a_copay_mcs_endd_int1_t1,
                                pbp_b1a_copay_mcs_amt_int2_t1, pbp_b1a_copay_mcs_bgnd_int2_t1,pbp_b1a_copay_mcs_endd_int2_t1,
                                pbp_b1a_copay_mcs_amt_int3_t1, pbp_b1a_copay_mcs_bgnd_int3_t1,pbp_b1a_copay_mcs_endd_int3_t1,
                                pbp_b1a_copay_ad_intrvl_num_t1, pbp_b1a_copay_ad_amt_int1_t1, pbp_b1a_copay_ad_bgnd_int1_t1, pbp_b1a_copay_ad_endd_int1_t1):
        if pbp_b1a_coins_yn == 1 or pbp_b1a_copay_yn == 1:
            if pbp_a_special_need_plan_type == 3 and pbp_a_dsnp_zerodollar == 1:
                return '$0 copay' 
            if pbp_a_special_need_plan_type == 3 and pbp_a_snp_state_cvg_yn == 1:
                return '$0 copay' 
            if pbp_b1a_mc_coins_cstshr_yn_t1 == 1 or pbp_b1a_mc_copay_cstshr_yn_t1 == 1:
                if pbp_a_special_need_plan_type == 3:
                    return self.ORIGINAL_MEDICARE_COST_DSNP
                return self.ORIGINAL_MEDICARE_COST
            if pbp_b1a_coins_yn == 1:
                return self.get_1a_tier_coinsurance(pbp_a_special_need_plan_type, pbp_b1a_coins_mcs_int_num_t1, pbp_b1a_coins_mcs_pct_int1_t1, pbp_b1a_coins_mcs_bgnd_int1_t1,pbp_b1a_coins_mcs_endd_int1_t1,
                            pbp_b1a_coins_mcs_pct_int2_t1, pbp_b1a_coins_mcs_bgnd_int2_t1,pbp_b1a_coins_mcs_endd_int2_t1,
                            pbp_b1a_coins_mcs_pct_int3_t1, pbp_b1a_coins_mcs_bgnd_int3_t1,pbp_b1a_coins_mcs_endd_int3_t)
            else:
                return self.get_1a_tier_copay(pbp_a_special_need_plan_type, pbp_b1a_copay_mcs_amt_t1,
                    pbp_b1a_copay_mcs_int_num_t1, pbp_b1a_copay_mcs_amt_int1_t1, pbp_b1a_copay_mcs_bgnd_int1_t1,pbp_b1a_copay_mcs_endd_int1_t1,
                            pbp_b1a_copay_mcs_amt_int2_t1, pbp_b1a_copay_mcs_bgnd_int2_t1,pbp_b1a_copay_mcs_endd_int2_t1,
                            pbp_b1a_copay_mcs_amt_int3_t1, pbp_b1a_copay_mcs_bgnd_int3_t1,pbp_b1a_copay_mcs_endd_int3_t1,
                            pbp_b1a_copay_ad_intrvl_num_t1, pbp_b1a_copay_ad_amt_int1_t1, pbp_b1a_copay_ad_bgnd_int1_t1, pbp_b1a_copay_ad_endd_int1_t1)
        else:
            return '$0 copay'
            
    def get_mc_inn_tier_benefit_text(self, pbp_a_special_need_plan_type, pbp_a_dsnp_zerodollar, pbp_a_snp_state_cvg_yn, pbp_b1a_cost_vary_tier_num,
                                pbp_b1a_coins_yn
    ,pbp_b1a_copay_yn,pbp_b1a_mc_coins_cstshr_yn_t1,pbp_b1a_coins_mcs_pct_t1,pbp_b1a_coins_mcs_int_num_t1,pbp_b1a_coins_mcs_pct_int1_t1,pbp_b1a_coins_mcs_bgnd_int1_t1,pbp_b1a_coins_mcs_endd_int1_t1,pbp_b1a_coins_mcs_pct_int2_t1
    ,pbp_b1a_coins_mcs_bgnd_int2_t1,pbp_b1a_coins_mcs_endd_int2_t1,pbp_b1a_coins_mcs_pct_int3_t1,pbp_b1a_coins_mcs_bgnd_int3_t1,pbp_b1a_coins_mcs_endd_int3_t1,pbp_b1a_mc_copay_cstshr_yn_t1,pbp_b1a_copay_mcs_amt_t1
    ,pbp_b1a_copay_mcs_int_num_t1,pbp_b1a_copay_mcs_amt_int1_t1,pbp_b1a_copay_mcs_bgnd_int1_t1,pbp_b1a_copay_mcs_endd_int1_t1,pbp_b1a_copay_mcs_amt_int2_t1,pbp_b1a_copay_mcs_bgnd_int2_t1,pbp_b1a_copay_mcs_endd_int2_t1
    ,pbp_b1a_copay_mcs_amt_int3_t1,pbp_b1a_copay_mcs_bgnd_int3_t1,pbp_b1a_copay_mcs_endd_int3_t1, pbp_b1a_copay_ad_intrvl_num_t1, pbp_b1a_copay_ad_amt_int1_t1, pbp_b1a_copay_ad_bgnd_int1_t1, pbp_b1a_copay_ad_endd_int1_t1
    ,pbp_b1a_mc_coins_cstshr_yn_t2,pbp_b1a_coins_mcs_pct_t2,pbp_b1a_coins_mcs_int_num_t2,pbp_b1a_coins_mcs_pct_int1_t2,pbp_b1a_coins_mcs_bgnd_int1_t2,pbp_b1a_coins_mcs_endd_int1_t2,pbp_b1a_coins_mcs_pct_int2_t2,pbp_b1a_coins_mcs_bgnd_int2_t2
    ,pbp_b1a_coins_mcs_endd_int2_t2,pbp_b1a_coins_mcs_pct_int3_t2,pbp_b1a_coins_mcs_bgnd_int3_t2,pbp_b1a_coins_mcs_endd_int3_t2,pbp_b1a_mc_copay_cstshr_yn_t2,pbp_b1a_copay_mcs_amt_t2,pbp_b1a_copay_mcs_int_num_t2
    ,pbp_b1a_copay_mcs_amt_int1_t2,pbp_b1a_copay_mcs_bgnd_int1_t2,pbp_b1a_copay_mcs_endd_int1_t2,pbp_b1a_copay_mcs_amt_int2_t2,pbp_b1a_copay_mcs_bgnd_int2_t2,pbp_b1a_copay_mcs_endd_int2_t2,pbp_b1a_copay_mcs_amt_int3_t2
    ,pbp_b1a_copay_mcs_bgnd_int3_t2,pbp_b1a_copay_mcs_endd_int3_t2, pbp_b1a_copay_ad_intrvl_num_t2, pbp_b1a_copay_ad_amt_int1_t2, pbp_b1a_copay_ad_bgnd_int1_t2, pbp_b1a_copay_ad_endd_int1_t2, pbp_b1a_ad_cost_vary_tiers_yn):
        inn_benefit = self.get_1a_inn_tier_benefit(pbp_a_special_need_plan_type, pbp_a_dsnp_zerodollar, pbp_a_snp_state_cvg_yn, 
                                pbp_b1a_coins_yn, pbp_b1a_mc_coins_cstshr_yn_t1, 
                                pbp_b1a_coins_mcs_int_num_t1, pbp_b1a_coins_mcs_pct_int1_t1, pbp_b1a_coins_mcs_bgnd_int1_t1,pbp_b1a_coins_mcs_endd_int1_t1,
                                pbp_b1a_coins_mcs_pct_int2_t1, pbp_b1a_coins_mcs_bgnd_int2_t1,pbp_b1a_coins_mcs_endd_int2_t1,
                                pbp_b1a_coins_mcs_pct_int3_t1, pbp_b1a_coins_mcs_bgnd_int3_t1,pbp_b1a_coins_mcs_endd_int3_t1,
                                pbp_b1a_copay_yn, pbp_b1a_copay_mcs_amt_t1, pbp_b1a_mc_copay_cstshr_yn_t1, 
                                pbp_b1a_copay_mcs_int_num_t1, pbp_b1a_copay_mcs_amt_int1_t1, pbp_b1a_copay_mcs_bgnd_int1_t1,pbp_b1a_copay_mcs_endd_int1_t1,
                                pbp_b1a_copay_mcs_amt_int2_t1, pbp_b1a_copay_mcs_bgnd_int2_t1,pbp_b1a_copay_mcs_endd_int2_t1,
                                pbp_b1a_copay_mcs_amt_int3_t1, pbp_b1a_copay_mcs_bgnd_int3_t1,pbp_b1a_copay_mcs_endd_int3_t1,
                                pbp_b1a_copay_ad_intrvl_num_t1, pbp_b1a_copay_ad_amt_int1_t1, pbp_b1a_copay_ad_bgnd_int1_t1, pbp_b1a_copay_ad_endd_int1_t1)
        if pbp_b1a_ad_cost_vary_tiers_yn == 2 and pbp_b1a_cost_vary_tier_num == 2:  
            t2_inn_benefit = self.get_1a_inn_tier_benefit(pbp_a_special_need_plan_type, pbp_a_dsnp_zerodollar, pbp_a_snp_state_cvg_yn, 
                                pbp_b1a_coins_yn, pbp_b1a_mc_coins_cstshr_yn_t2, 
                                pbp_b1a_coins_mcs_int_num_t2, pbp_b1a_coins_mcs_pct_int1_t2, pbp_b1a_coins_mcs_bgnd_int1_t2,pbp_b1a_coins_mcs_endd_int1_t2,
                                pbp_b1a_coins_mcs_pct_int2_t2, pbp_b1a_coins_mcs_bgnd_int2_t2,pbp_b1a_coins_mcs_endd_int2_t2,
                                pbp_b1a_coins_mcs_pct_int3_t2, pbp_b1a_coins_mcs_bgnd_int3_t2,pbp_b1a_coins_mcs_endd_int3_t2,
                                pbp_b1a_copay_yn, pbp_b1a_copay_mcs_amt_t2, pbp_b1a_mc_copay_cstshr_yn_t2, 
                                pbp_b1a_copay_mcs_int_num_t2, pbp_b1a_copay_mcs_amt_int1_t2, pbp_b1a_copay_mcs_bgnd_int1_t2,pbp_b1a_copay_mcs_endd_int1_t2,
                                pbp_b1a_copay_mcs_amt_int2_t2, pbp_b1a_copay_mcs_bgnd_int2_t2,pbp_b1a_copay_mcs_endd_int2_t2,
                                pbp_b1a_copay_mcs_amt_int3_t2, pbp_b1a_copay_mcs_bgnd_int3_t2,pbp_b1a_copay_mcs_endd_int3_t2,
                                pbp_b1a_copay_ad_intrvl_num_t2, pbp_b1a_copay_ad_amt_int1_t2, pbp_b1a_copay_ad_bgnd_int1_t2, pbp_b1a_copay_ad_endd_int1_t2)
            inn_benefit = f'Tier 1<br/>{inn_benefit}<br/>Tier 2<br/>{t2_inn_benefit}'
        return inn_benefit

    def get_1a_oon_coinsurance(self, pbp_c_oon_coins_iha_mc_cost_yn, pbp_c_oon_coins_iha_intrvl_num, pbp_c_oon_coins_iha_ps_amt,
                            pbp_c_oon_coins_iha_pct_i1, pbp_c_oon_coins_iha_bgnd_i1, pbp_c_oon_coins_iha_endd_i1,
                            pbp_c_oon_coins_iha_pct_i2, pbp_c_oon_coins_iha_bgnd_i2,pbp_c_oon_coins_iha_endd_i2,
                            pbp_c_oon_coins_iha_pct_i3, pbp_c_oon_coins_iha_bgnd_i3,pbp_c_oon_coins_iha_endd_i3):
        if pbp_c_oon_coins_iha_mc_cost_yn == 1:
            return self.ORIGINAL_MEDICARE_COST
        if not np.isnan(pbp_c_oon_coins_iha_intrvl_num):
            if pbp_c_oon_coins_iha_intrvl_num == 1:
                if pbp_c_oon_coins_iha_ps_amt == 0:
                    return '$0 copay per stay'
                return f'{int(pbp_c_oon_coins_iha_ps_amt)}% per stay'
            elif pbp_c_oon_coins_iha_intrvl_num > 1 and pbp_c_oon_coins_iha_intrvl_num <= 4:
                tier_coinsurance = self.get_1a_tier_coinsurance(2,pbp_c_oon_coins_iha_intrvl_num, pbp_c_oon_coins_iha_pct_i1, pbp_c_oon_coins_iha_bgnd_i1, pbp_c_oon_coins_iha_endd_i1,
                                pbp_c_oon_coins_iha_pct_i2, pbp_c_oon_coins_iha_bgnd_i2,pbp_c_oon_coins_iha_endd_i2,
                                pbp_c_oon_coins_iha_pct_i3, pbp_c_oon_coins_iha_bgnd_i3,pbp_c_oon_coins_iha_endd_i3)
                if pbp_c_oon_coins_iha_ps_amt > 0:
                    tier_coinsurance = f'{int(pbp_c_oon_coins_iha_ps_amt)}% per stay <br/>' + tier_coinsurance
                return tier_coinsurance
        return 'Not Applicable'
            
    def get_1a_oon_copay(self, pbp_c_oon_copay_iha_mc_cost_yn, pbp_c_oon_copay_iha_intrvl_num, pbp_c_oon_copay_iha_ps_amt, 
                        pbp_c_oon_copay_iha_amt_i1, pbp_c_oon_copay_iha_bgnd_i1, pbp_c_oon_copay_iha_endd_i1,
                            pbp_c_oon_copay_iha_amt_i2, pbp_c_oon_copay_iha_bgnd_i2,pbp_c_oon_copay_iha_endd_i2,
                            pbp_c_oon_copay_iha_amt_i3, pbp_c_oon_copay_iha_bgnd_i3,pbp_c_oon_copay_iha_endd_i3):        
        if pbp_c_oon_copay_iha_mc_cost_yn == 1:
            return self.ORIGINAL_MEDICARE_COST
        if pbp_c_oon_copay_iha_intrvl_num == 1:
            if pbp_c_oon_copay_iha_ps_amt == 0:
                return '$0 copay per stay'
            return f'{self.convert_to_currency_no_decimal(pbp_c_oon_copay_iha_ps_amt)} per stay'
        elif pbp_c_oon_copay_iha_intrvl_num > 1 and pbp_c_oon_copay_iha_intrvl_num <= 4:
            return  self.get_1a_tier_copay(2, pbp_c_oon_copay_iha_ps_amt,
                    pbp_c_oon_copay_iha_intrvl_num, pbp_c_oon_copay_iha_amt_i1, pbp_c_oon_copay_iha_bgnd_i1, pbp_c_oon_copay_iha_endd_i1,
                            pbp_c_oon_copay_iha_amt_i2, pbp_c_oon_copay_iha_bgnd_i2,pbp_c_oon_copay_iha_endd_i2,
                            pbp_c_oon_copay_iha_amt_i3, pbp_c_oon_copay_iha_bgnd_i3,pbp_c_oon_copay_iha_endd_i3,
                            0, 0, 0, 0)
        return ''

    def get_mc_onn_tier_benefit_text(self,pbp_c_oon_coins_ihs_yn, pbp_c_oon_coins_iha_mc_cost_yn, pbp_c_oon_coins_iha_pct, pbp_c_oon_coins_iha_intrvl_num, 
        pbp_c_oon_coins_iha_pct_i1, pbp_c_oon_coins_iha_bgnd_i1, pbp_c_oon_coins_iha_endd_i1,
        pbp_c_oon_coins_iha_pct_i2, pbp_c_oon_coins_iha_bgnd_i2,pbp_c_oon_coins_iha_endd_i2,
        pbp_c_oon_coins_iha_pct_i3, pbp_c_oon_coins_iha_bgnd_i3,pbp_c_oon_coins_iha_endd_i3,
        pbp_c_oon_copay_ihs_yn,  pbp_c_oon_copay_iha_mc_cost_yn, pbp_c_oon_copay_iha_ps_amt,pbp_c_oon_copay_iha_intrvl_num,
        pbp_c_oon_copay_iha_amt_i1, pbp_c_oon_copay_iha_bgnd_i1, pbp_c_oon_copay_iha_endd_i1,
        pbp_c_oon_copay_iha_amt_i2, pbp_c_oon_copay_iha_bgnd_i2,pbp_c_oon_copay_iha_endd_i2,
        pbp_c_oon_copay_iha_amt_i3, pbp_c_oon_copay_iha_bgnd_i3,pbp_c_oon_copay_iha_endd_i3,
        pbp_c_pos_yn, pbp_c_pos_mc_bendesc_subcats,
        pbp_c_pos_coins_ihs_yn, pbp_c_pos_coins_iha_mc_cost_yn, pbp_c_pos_coins_iha_intrvl_num, pbp_c_pos_coins_iha_pct,
        pbp_c_pos_coins_iha_pct_i1, pbp_c_pos_coins_iha_bgnd_i1, pbp_c_pos_coins_iha_endd_i1,
        pbp_c_pos_coins_iha_pct_i2, pbp_c_pos_coins_iha_bgnd_i2,pbp_c_pos_coins_iha_endd_i2,
        pbp_c_pos_coins_iha_pct_i3, pbp_c_pos_coins_iha_bgnd_i3,pbp_c_pos_coins_iha_endd_i3,
        pbp_c_pos_copay_ihs_yn, pbp_c_pos_copay_iha_mc_cost_yn, pbp_c_pos_copay_iha_intrvl_num, pbp_c_pos_copay_iha_ps_amt,
        pbp_c_pos_copay_iha_amt_i1, pbp_c_pos_copay_iha_bgnd_i1, pbp_c_pos_copay_iha_endd_i1,
        pbp_c_pos_copay_iha_amt_i2, pbp_c_pos_copay_iha_bgnd_i2,pbp_c_pos_copay_iha_endd_i2,
        pbp_c_pos_copay_iha_amt_i3, pbp_c_pos_copay_iha_bgnd_i3,pbp_c_pos_copay_iha_endd_i3):
        if pbp_c_oon_coins_ihs_yn != 1 and pbp_c_oon_copay_ihs_yn != 1 and pbp_c_pos_yn != 1:
            return ''
        oon_benefit_text = 'Not Applicable'
        #handle Copay & Coinsurance are 1 
        # check pbp_c_oon_coins_iha_intrvl_num
        if pbp_c_oon_coins_ihs_yn == 1 and pbp_c_oon_copay_ihs_yn == 1:
            if np.isnan(pbp_c_oon_coins_iha_intrvl_num):
                pbp_c_oon_coins_ihs_yn = 2
        
        if pbp_c_oon_coins_ihs_yn == 1:
            oon_benefit_text = self.get_1a_oon_coinsurance(pbp_c_oon_coins_iha_mc_cost_yn, pbp_c_oon_coins_iha_intrvl_num, pbp_c_oon_coins_iha_pct,
                                        pbp_c_oon_coins_iha_pct_i1, pbp_c_oon_coins_iha_bgnd_i1, pbp_c_oon_coins_iha_endd_i1,
                                        pbp_c_oon_coins_iha_pct_i2, pbp_c_oon_coins_iha_bgnd_i2,pbp_c_oon_coins_iha_endd_i2,
                                        pbp_c_oon_coins_iha_pct_i3, pbp_c_oon_coins_iha_bgnd_i3,pbp_c_oon_coins_iha_endd_i3)
        elif pbp_c_oon_copay_ihs_yn == 1:
            oon_benefit_text = self.get_1a_oon_copay(pbp_c_oon_copay_iha_mc_cost_yn, pbp_c_oon_copay_iha_intrvl_num, pbp_c_oon_copay_iha_ps_amt,
                                    pbp_c_oon_copay_iha_amt_i1, pbp_c_oon_copay_iha_bgnd_i1, pbp_c_oon_copay_iha_endd_i1,
                                    pbp_c_oon_copay_iha_amt_i2, pbp_c_oon_copay_iha_bgnd_i2,pbp_c_oon_copay_iha_endd_i2,
                                    pbp_c_oon_copay_iha_amt_i3, pbp_c_oon_copay_iha_bgnd_i3,pbp_c_oon_copay_iha_endd_i3)
        elif np.isnan(pbp_c_oon_coins_ihs_yn) and np.isnan(pbp_c_oon_copay_ihs_yn):
            if pbp_c_pos_yn == 1:
                if pbp_c_pos_coins_ihs_yn == 1:
                    oon_benefit_text = self.get_1a_oon_coinsurance(pbp_c_pos_coins_iha_mc_cost_yn, pbp_c_pos_coins_iha_intrvl_num, pbp_c_pos_coins_iha_pct,
                                                pbp_c_pos_coins_iha_pct_i1, pbp_c_pos_coins_iha_bgnd_i1, pbp_c_pos_coins_iha_endd_i1,
                                                pbp_c_pos_coins_iha_pct_i2, pbp_c_pos_coins_iha_bgnd_i2,pbp_c_pos_coins_iha_endd_i2,
                                                pbp_c_pos_coins_iha_pct_i3, pbp_c_pos_coins_iha_bgnd_i3,pbp_c_pos_coins_iha_endd_i3)
                elif pbp_c_pos_copay_ihs_yn == 1:
                    oon_benefit_text =  self.get_1a_oon_copay(pbp_c_pos_copay_iha_mc_cost_yn, pbp_c_pos_copay_iha_intrvl_num, pbp_c_pos_copay_iha_ps_amt,
                                            pbp_c_pos_copay_iha_amt_i1, pbp_c_pos_copay_iha_bgnd_i1, pbp_c_pos_copay_iha_endd_i1,
                                            pbp_c_pos_copay_iha_amt_i2, pbp_c_pos_copay_iha_bgnd_i2,pbp_c_pos_copay_iha_endd_i2,
                                            pbp_c_pos_copay_iha_amt_i3, pbp_c_pos_copay_iha_bgnd_i3,pbp_c_pos_copay_iha_endd_i3)
                elif pbp_c_pos_coins_ihs_yn == 2 and pbp_c_pos_copay_ihs_yn == 2:
                    oon_benefit_text = '$0 copay'
                # elif isinstance(pbp_c_pos_mc_bendesc_subcats, str):
                #    if self.has_benefits_in(pbp_c_pos_mc_bendesc_subcats, self.CATEGORY_CODE):
                #        oon_benefit_text = '$0 copay'
                else:
                    oon_benefit_text = 'Not Applicable'
        # if oon_benefit_text != None and len(oon_benefit_text) > 0 and pbp_b1a_auth_yn == 1:
        #    oon_benefit_text += '(Limits apply)'
        return oon_benefit_text

class Benefit_MC(Benefit):
    '''
    No bendesc_yn and benedesc_ehc
    No coins_ehc and copay_ehc
    '''
    
    def get_9a_inn_copay_text(self, pbp_b9a_copay_ohs_amt_min,pbp_b9a_copay_ohs_amt_max):
        if np.isnan(pbp_b9a_copay_ohs_amt_min) and np.isnan(pbp_b9a_copay_ohs_amt_max):
            benefit_text =  f'$0 copay'
        elif pbp_b9a_copay_ohs_amt_min < pbp_b9a_copay_ohs_amt_max:
            benefit_text = f'{self.convert_to_currency_no_decimal(pbp_b9a_copay_ohs_amt_min)}-{self.convert_to_currency_no_decimal(pbp_b9a_copay_ohs_amt_max)} copay'
        elif pbp_b9a_copay_ohs_amt_min == 0:
            return  '$0 copay'
        else:
            benefit_text = f'{self.convert_to_currency_no_decimal(pbp_b9a_copay_ohs_amt_min)} copay'
        return benefit_text

    def get_9a_inn_coins_text(self, pbp_b9a_coins_ohs_pct_min,pbp_b9a_coins_ohs_pct_max):
        if np.isnan(pbp_b9a_coins_ohs_pct_min) and np.isnan(pbp_b9a_coins_ohs_pct_max):
            return f'$0 copay'
        elif pbp_b9a_coins_ohs_pct_min < pbp_b9a_coins_ohs_pct_max:
            benefit_text = f'{int(pbp_b9a_coins_ohs_pct_min)}-{int(pbp_b9a_coins_ohs_pct_max)}% coinsurance'
        elif pbp_b9a_coins_ohs_pct_min == 0:
            return  '$0 copay'
        else:
            benefit_text = f'{int(pbp_b9a_coins_ohs_pct_max)}% coinsurance'
        return benefit_text
        

    def get_oon_benefit_text(self, pbp_c_oon_yn, 
        pbp_c_oon_outpt_coins_yn,pbp_c_oon_outpt_coins_min_pct,pbp_c_oon_outpt_coins_max_pct,
        pbp_c_oon_outpt_copay_yn,pbp_c_oon_outpt_copay_min_amt,pbp_c_oon_outpt_copay_max_amt,
        pbp_c_pos_outpt_coins_yn,pbp_c_pos_outpt_coins_min_pct,pbp_c_pos_outpt_coins_max_pct,
        pbp_c_pos_outpt_copay_yn,pbp_c_pos_outpt_copay_min_amt,pbp_c_pos_outpt_copay_max_amt):
        oon_benefit_text = ''
        if pbp_c_oon_yn == 1:
            if pbp_c_oon_outpt_coins_yn == 2 and pbp_c_oon_outpt_copay_yn == 2:
                oon_benefit_text = '$0 copay'
            elif pbp_c_oon_outpt_coins_yn == 1 and pbp_c_oon_outpt_copay_yn == 1:
                oon_coins_benefit_text = self.get_9a_inn_coins_text(pbp_c_oon_outpt_coins_min_pct, pbp_c_oon_outpt_coins_max_pct)
                oon_copay_benefit_text = self.get_9a_inn_copay_text(pbp_c_oon_outpt_copay_min_amt, pbp_c_oon_outpt_copay_max_amt)
                if oon_coins_benefit_text == oon_copay_benefit_text:
                    oon_benefit_text = oon_copay_benefit_text
                else:
                    oon_benefit_text = oon_copay_benefit_text + " or " + oon_coins_benefit_text
            elif pbp_c_oon_outpt_coins_yn == 1:
                oon_benefit_text = self.get_9a_inn_coins_text(pbp_c_oon_outpt_coins_min_pct, pbp_c_oon_outpt_coins_max_pct)
            elif pbp_c_oon_outpt_copay_yn == 1:
                oon_benefit_text = self.get_9a_inn_copay_text(pbp_c_oon_outpt_copay_min_amt, pbp_c_oon_outpt_copay_max_amt)
        elif pbp_c_pos_outpt_coins_yn == 1 or pbp_c_pos_outpt_copay_yn == 1:
            if pbp_c_pos_outpt_coins_yn == 1 and pbp_c_pos_outpt_copay_yn == 1:
                oon_coins_benefit_text = self.get_9a_inn_coins_text(pbp_c_pos_outpt_coins_min_pct, pbp_c_pos_outpt_coins_max_pct)
                oon_copay_benefit_text = self.get_9a_inn_copay_text(pbp_c_pos_outpt_copay_min_amt, pbp_c_pos_outpt_copay_max_amt)
                oon_benefit_text = oon_copay_benefit_text + " or " + oon_coins_benefit_text
            elif pbp_c_pos_outpt_copay_yn == 1:
                oon_benefit_text = self.get_9a_inn_copay_text(pbp_c_pos_outpt_copay_min_amt, pbp_c_pos_outpt_copay_max_amt)
            elif pbp_c_pos_outpt_coins_yn == 1:
                oon_benefit_text = self.get_9a_inn_coins_text(pbp_c_pos_outpt_coins_min_pct, pbp_c_pos_outpt_coins_max_pct)
        elif pbp_c_pos_outpt_coins_yn == 2 and pbp_c_pos_outpt_copay_yn == 2:
            oon_benefit_text = '$0 copay'
        return oon_benefit_text
    
    def get_mc_inn_benefit_text(self,pbp_a_special_need_plan_type, pbp_a_dsnp_zerodollar, pbp_a_snp_state_cvg_yn, 
                                pbp_b4b_coins_yn,pbp_b4a_coins_pct_mc_min,pbp_b4a_coins_pct_mc_max,
                                pbp_b4b_copay_yn,pbp_b4a_copay_amt_mc_min,pbp_b4a_copay_amt_mc_max):
        benefit_text = ''
        if not np.isnan(pbp_b4a_copay_amt_mc_min) and not np.isnan(pbp_b4a_coins_pct_mc_min):
            benefit_copay_text = self.get_9a_inn_copay_text(pbp_b4a_copay_amt_mc_min,pbp_b4a_copay_amt_mc_max)
            benefit_coins_text = self.get_9a_inn_coins_text(pbp_b4a_coins_pct_mc_min,pbp_b4a_coins_pct_mc_max)
            if benefit_copay_text.startswith('$0-') and benefit_coins_text == f'$0 copay':
                benefit_text = benefit_copay_text
            elif benefit_copay_text == benefit_coins_text:
                benefit_text = benefit_copay_text
            else:
                benefit_text = benefit_copay_text + " or " + benefit_coins_text
        elif not np.isnan(pbp_b4a_copay_amt_mc_min):  
            benefit_text = self.get_9a_inn_copay_text(pbp_b4a_copay_amt_mc_min,pbp_b4a_copay_amt_mc_max)
        elif not np.isnan(pbp_b4a_coins_pct_mc_min):
            benefit_text = self.get_9a_inn_coins_text(pbp_b4a_coins_pct_mc_min,pbp_b4a_coins_pct_mc_max)
        elif pbp_b4b_copay_yn == 2 and pbp_b4b_coins_yn == 2:
            benefit_text =  '$0 copay'
        elif pbp_b4b_copay_yn == 1 and np.isnan(pbp_b4a_copay_amt_mc_min):
            benefit_text =  '$0 copay'
        elif pbp_b4b_coins_yn == 1 and np.isnan(pbp_b4a_coins_pct_mc_min):
            benefit_text =  '$0 copay'
        else:
            return 'Not covered'
        if benefit_text not in ['', '$0 copay', 'Covered under office visit']:
            if pbp_a_special_need_plan_type == 3 and pbp_a_dsnp_zerodollar == 1:
                return '$0 copay'
            if pbp_a_special_need_plan_type == 3 and pbp_a_snp_state_cvg_yn == 1:
                return '$0 copay'
            if pbp_a_special_need_plan_type == 3 and '$0 copay' not in benefit_text:
                if pbp_b4b_copay_yn == 1:
                    benefit_text = '$0 or ' + benefit_text
                else:
                    benefit_text = f'0% or ' + benefit_text
        return benefit_text
         
    @staticmethod
    def get_OON_text(x):
        return Benefit_MC().get_oon_benefit_text(x.pbp_c_oon_yn,
                                                x.pbp_c_oon_outpt_coins_yn,x.pbp_c_oon_outpt_coins_min_pct,x.pbp_c_oon_outpt_coins_max_pct,
                                                x.pbp_c_oon_outpt_copay_yn,x.pbp_c_oon_outpt_copay_min_amt,x.pbp_c_oon_outpt_copay_max_amt,
                                                x.pbp_c_pos_outpt_coins_yn,x.pbp_c_pos_outpt_coins_min_pct,x.pbp_c_pos_outpt_coins_max_pct,
                                                x.pbp_c_pos_outpt_copay_yn,x.pbp_c_pos_outpt_copay_min_amt,x.pbp_c_pos_outpt_copay_max_amt)
    
class Benefit_MC_EHC(Benefit_MC):
    '''
    EHC 
    1 in 2	Medicare-covered Outpatient Hospital Services
    1 in 1	Medicare-covered Observation Services
    '''
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2
    
        
        
    def get_mc_ehc_inn_benefit_text(self, pbp_a_special_need_plan_type, pbp_a_dsnp_zerodollar, pbp_a_snp_state_cvg_yn,
        pbp_b9a_copay_yn,pbp_b9a_copay_ehc,pbp_b9a_copay_ohs_amt_min,pbp_b9a_copay_ohs_amt_max, 
        pbp_b9a_coins_yn,pbp_b9a_coins_ehc,pbp_b9a_coins_ohs_pct_min,pbp_b9a_coins_ohs_pct_max):
        benefit_text = ''
        if np.isnan(pbp_b9a_copay_yn) and np.isnan(pbp_b9a_coins_yn):
            return 'Not covered'
        if pbp_a_special_need_plan_type == 3 and pbp_a_dsnp_zerodollar == 1:
            benefit_text =  '$0 copay'
        elif pbp_a_special_need_plan_type == 3 and pbp_a_snp_state_cvg_yn == 1:
            benefit_text =  '$0 copay'
        elif pbp_b9a_copay_yn == 2 and pbp_b9a_coins_yn == 2:
            benefit_text =  '$0 copay'
        elif pbp_b9a_copay_yn == 1 and pbp_b9a_copay_ohs_amt_min >=  0 and self.is_there_a_copayment_for_service(pbp_b9a_copay_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE)  == 1 \
            and pbp_b9a_coins_yn == 1 and pbp_b9a_coins_ohs_pct_min >= 0 and self.is_there_a_copayment_for_service(pbp_b9a_coins_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE) == 1:
            benefit_copay_text = self.get_9a_inn_copay_text(pbp_b9a_copay_ohs_amt_min,pbp_b9a_copay_ohs_amt_max)
            benefit_coins_text = self.get_9a_inn_coins_text(pbp_b9a_coins_ohs_pct_min,pbp_b9a_coins_ohs_pct_max)
            benefit_text = benefit_copay_text + " or " + benefit_coins_text
        elif pbp_b9a_copay_yn == 1 and pbp_b9a_copay_ohs_amt_min >=  0 and self.is_there_a_copayment_for_service(pbp_b9a_copay_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE) == 1:
            benefit_text = self.get_9a_inn_copay_text(pbp_b9a_copay_ohs_amt_min,pbp_b9a_copay_ohs_amt_max)
        elif pbp_b9a_coins_yn == 1 and pbp_b9a_coins_ohs_pct_min >= 0 and self.is_there_a_copayment_for_service(pbp_b9a_coins_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE) == 1:
            benefit_text = self.get_9a_inn_coins_text(pbp_b9a_coins_ohs_pct_min,pbp_b9a_coins_ohs_pct_max)
        elif pbp_b9a_copay_yn == 1 and self.is_there_a_copayment_for_service(pbp_b9a_copay_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE) != 1:
            benefit_text =  '$0 copay'
        elif pbp_b9a_coins_yn == 1 and self.is_there_a_copayment_for_service(pbp_b9a_coins_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE) != 1:
            benefit_text =  '$0 copay'
        
        if benefit_text not in ['', '$0 copay']:
            if pbp_a_special_need_plan_type == 3 and '$0 copay' not in benefit_text:
                if pbp_b9a_copay_yn == 1:
                    benefit_text = '$0 or ' + benefit_text
                else:
                    benefit_text = f'0% or ' + benefit_text
        return benefit_text

class Benefit_NMC(Benefit_MC):
    def get_nmc_inn_benefit_text(self, pbp_a_special_need_plan_type, pbp_a_dsnp_zerodollar, pbp_a_snp_state_cvg_yn, 
                                pbp_b16a_copay_cserv_sc_pov_yn,pbp_b16a_coins_cserv_sc_pov_yn, 
                                pbp_b16a_bendesc_yn, pbp_b16a_bendesc_ehc,
        pbp_b16a_coins_yn,pbp_b16a_coins_ehc,pbp_b16a_coins_pct_dx,pbp_b16a_coins_pct_maxdx, 
        pbp_b16a_copay_yn,pbp_b16a_copay_ehc,pbp_b16a_copay_amt_dxmin,pbp_b16a_copay_amt_dxmax):
        benefit_text = ''
        if not np.isnan(pbp_b16a_copay_amt_dxmin) and not np.isnan(pbp_b16a_coins_pct_dx):
            benefit_copay_text = self.get_9a_inn_copay_text(pbp_b16a_copay_amt_dxmin,pbp_b16a_copay_amt_dxmax)
            benefit_coins_text = self.get_9a_inn_coins_text(pbp_b16a_coins_pct_dx,pbp_b16a_coins_pct_maxdx)
            if benefit_copay_text.startswith('$0-') and benefit_coins_text == f'$0 copay':
                benefit_text = benefit_copay_text
            elif benefit_copay_text == benefit_coins_text:
                benefit_text = benefit_copay_text
            else:
                benefit_text = benefit_copay_text + " or " + benefit_coins_text
        elif not np.isnan(pbp_b16a_copay_amt_dxmin):
            benefit_text = self.get_9a_inn_copay_text(pbp_b16a_copay_amt_dxmin,pbp_b16a_copay_amt_dxmax)
        elif not np.isnan(pbp_b16a_coins_pct_dx):
            benefit_text = self.get_9a_inn_coins_text(pbp_b16a_coins_pct_dx,pbp_b16a_coins_pct_maxdx)
        elif pbp_b16a_bendesc_yn == 1:
            if self.is_there_a_copayment_for_service(pbp_b16a_bendesc_ehc, self.BENEDESC_EHC_TOTAL_SERVICE, self.BENEDESC_EHC_SERVICE) == 1:
                if pbp_b16a_copay_cserv_sc_pov_yn == 1 or pbp_b16a_coins_cserv_sc_pov_yn == 1:
                    benefit_text = 'Covered under office visit'
                else:
                    benefit_text = '$0 copay'
            else:
                return 'Not covered'
        elif pbp_b16a_copay_yn == 1:
            if self.is_there_a_copayment_for_service(pbp_b16a_coins_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE) == 1:
                if pbp_b16a_copay_cserv_sc_pov_yn == 1:
                    benefit_text = 'Covered under office visit'
                else:
                    benefit_text = '$0 copay'
            else:
                return 'Not covered'
        elif pbp_b16a_coins_yn == 1:
            if self.is_there_a_copayment_for_service(pbp_b16a_copay_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE) == 1:
                if pbp_b16a_coins_cserv_sc_pov_yn == 1:
                    benefit_text = 'Covered under office visit'
                else:
                    benefit_text = '$0 copay'
            else:
                return 'Not covered'
        else:
            if pbp_b16a_copay_yn == 2 and pbp_b16a_coins_yn == 2 and self.is_there_a_copayment_for_service(pbp_b16a_coins_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE) == 1 and self.is_there_a_copayment_for_service(pbp_b16a_copay_ehc, self.EHC_TOTAL_SERVICE, self.EHC_SERVICE) == 1:
                benefit_text = '$0 copay'
            else:
                return 'Not covered'
        
        if benefit_text not in ['', '$0 copay', 'Covered under office visit']:
            if pbp_a_special_need_plan_type == 3 and pbp_a_dsnp_zerodollar == 1:
                return '$0 copay'
            if pbp_a_special_need_plan_type == 3 and pbp_a_snp_state_cvg_yn == 1:
                return '$0 copay'
            if pbp_a_special_need_plan_type == 3 and '$0 copay' not in benefit_text:
                if pbp_b16a_copay_yn == 1:
                    benefit_text = '$0 or ' + benefit_text
                else:
                    benefit_text = f'0% or ' + benefit_text
        return benefit_text
        
    
# Benefit text per benefit service category
# MC Tiers: 1a, 2
# MC: 4a, 4b, 7a, 7c, 7d, 7e1, 7e2, 7i, 11a, 14a, 15_1_I, 
# MC EHC: 7b, 7e1, 7e2, 7h1, 7h2, 8a1, 8a2, 8b1, 8b3, 9a1, 10a1, 10a2, 11b1, 11c1,15_2, 15_3, 18a
# NMC: 10b1, 10b2, 13a, 13b, 13c, 16a1, 16a2, 16a3, 16a4, 17a1, 17b1, 17b2, 17b3, 17b4, 17b5, 18a1, 18a2, 18b1
    
class Benefit_1a(Benefit_MC_Tiers):
    @staticmethod
    def get_INN_text(x):
        return Benefit_1a().get_mc_inn_tier_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, x.pbp_b1a_cost_vary_tier_num,x.pbp_b1a_coins_yn
,x.pbp_b1a_copay_yn,x.pbp_b1a_mc_coins_cstshr_yn_t1,x.pbp_b1a_coins_mcs_pct_t1,x.pbp_b1a_coins_mcs_int_num_t1,x.pbp_b1a_coins_mcs_pct_int1_t1,x.pbp_b1a_coins_mcs_bgnd_int1_t1,x.pbp_b1a_coins_mcs_endd_int1_t1,x.pbp_b1a_coins_mcs_pct_int2_t1
,x.pbp_b1a_coins_mcs_bgnd_int2_t1,x.pbp_b1a_coins_mcs_endd_int2_t1,x.pbp_b1a_coins_mcs_pct_int3_t1,x.pbp_b1a_coins_mcs_bgnd_int3_t1,x.pbp_b1a_coins_mcs_endd_int3_t1,x.pbp_b1a_mc_copay_cstshr_yn_t1,x.pbp_b1a_copay_mcs_amt_t1
,x.pbp_b1a_copay_mcs_int_num_t1,x.pbp_b1a_copay_mcs_amt_int1_t1,x.pbp_b1a_copay_mcs_bgnd_int1_t1,x.pbp_b1a_copay_mcs_endd_int1_t1,x.pbp_b1a_copay_mcs_amt_int2_t1,x.pbp_b1a_copay_mcs_bgnd_int2_t1,x.pbp_b1a_copay_mcs_endd_int2_t1
,x.pbp_b1a_copay_mcs_amt_int3_t1,x.pbp_b1a_copay_mcs_bgnd_int3_t1,x.pbp_b1a_copay_mcs_endd_int3_t1, x.pbp_b1a_copay_ad_intrvl_num_t1, x.pbp_b1a_copay_ad_amt_int1_t1, x.pbp_b1a_copay_ad_bgnd_int1_t1, x.pbp_b1a_copay_ad_endd_int1_t1
,x.pbp_b1a_mc_coins_cstshr_yn_t2,x.pbp_b1a_coins_mcs_pct_t2,x.pbp_b1a_coins_mcs_int_num_t2,x.pbp_b1a_coins_mcs_pct_int1_t2,x.pbp_b1a_coins_mcs_bgnd_int1_t2,x.pbp_b1a_coins_mcs_endd_int1_t2,x.pbp_b1a_coins_mcs_pct_int2_t2,x.pbp_b1a_coins_mcs_bgnd_int2_t2
,x.pbp_b1a_coins_mcs_endd_int2_t2,x.pbp_b1a_coins_mcs_pct_int3_t2,x.pbp_b1a_coins_mcs_bgnd_int3_t2,x.pbp_b1a_coins_mcs_endd_int3_t2,x.pbp_b1a_mc_copay_cstshr_yn_t2,x.pbp_b1a_copay_mcs_amt_t2,x.pbp_b1a_copay_mcs_int_num_t2
,x.pbp_b1a_copay_mcs_amt_int1_t2,x.pbp_b1a_copay_mcs_bgnd_int1_t2,x.pbp_b1a_copay_mcs_endd_int1_t2,x.pbp_b1a_copay_mcs_amt_int2_t2,x.pbp_b1a_copay_mcs_bgnd_int2_t2,x.pbp_b1a_copay_mcs_endd_int2_t2,x.pbp_b1a_copay_mcs_amt_int3_t2
,x.pbp_b1a_copay_mcs_bgnd_int3_t2,x.pbp_b1a_copay_mcs_endd_int3_t2, x.pbp_b1a_copay_ad_intrvl_num_t2, x.pbp_b1a_copay_ad_amt_int1_t2, x.pbp_b1a_copay_ad_bgnd_int1_t2, x.pbp_b1a_copay_ad_endd_int1_t2, x.pbp_b1a_ad_cost_vary_tiers_yn)
    
    @staticmethod
    def get_OON_text(x): 
        return Benefit_1a().get_mc_onn_tier_benefit_text(x.pbp_c_oon_coins_ihs_yn, x.pbp_c_oon_coins_iha_mc_cost_yn, x.pbp_c_oon_coins_iha_pct, x.pbp_c_oon_coins_iha_intrvl_num, 
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
    x.pbp_c_pos_copay_iha_amt_i3, x.pbp_c_pos_copay_iha_bgnd_i3,x.pbp_c_pos_copay_iha_endd_i3)

class Benefit_2(Benefit_MC_Tiers):
    CATEGORY_CODE = '2'
    ORIGINAL_MEDICARE_COST = 'In 2024 the amounts for each benefit period are:<br />$0 copay for days 1 through 20<br />$204 copay per day for days 21 through 100'
    ORIGINAL_MEDICARE_COST_DSNP = 'In 2024 the amounts for each benefit period are $0 or:<br />$0 copay for days 1 through 20<br />$204 copay per day for days 21 through 100'

    @staticmethod
    def get_INN_text(x):
        return Benefit_2().get_mc_inn_tier_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,x.pbp_b2_cost_vary_tier_num,x.pbp_b2_coins_yn
    ,x.pbp_b2_copay_yn,x.pbp_b2_mc_coins_cstshr_yn_t1,x.pbp_b2_coins_mcs_pct_t1,x.pbp_b2_coins_mcs_int_num_t1,x.pbp_b2_coins_mcs_pct_int1_t1,x.pbp_b2_coins_mcs_bgnd_int1_t1,x.pbp_b2_coins_mcs_endd_int1_t1,x.pbp_b2_coins_mcs_pct_int2_t1
    ,x.pbp_b2_coins_mcs_bgnd_int2_t1,x.pbp_b2_coins_mcs_endd_int2_t1,x.pbp_b2_coins_mcs_pct_int3_t1,x.pbp_b2_coins_mcs_bgnd_int3_t1,x.pbp_b2_coins_mcs_endd_int3_t1,x.pbp_b2_mc_copay_cstshr_yn_t1,x.pbp_b2_copay_mcs_amt_t1
    ,x.pbp_b2_copay_mcs_int_num_t1,x.pbp_b2_copay_mcs_amt_int1_t1,x.pbp_b2_copay_mcs_bgnd_int1_t1,x.pbp_b2_copay_mcs_endd_int1_t1,x.pbp_b2_copay_mcs_amt_int2_t1,x.pbp_b2_copay_mcs_bgnd_int2_t1,x.pbp_b2_copay_mcs_endd_int2_t1
    ,x.pbp_b2_copay_mcs_amt_int3_t1,x.pbp_b2_copay_mcs_bgnd_int3_t1,x.pbp_b2_copay_mcs_endd_int3_t1, x.pbp_b2_copay_ad_intrvl_num_t1, x.pbp_b2_copay_ad_amt_int1_t1, x.pbp_b2_copay_ad_bgnd_int1_t1, x.pbp_b2_copay_ad_endd_int1_t1
    ,x.pbp_b2_mc_coins_cstshr_yn_t2,x.pbp_b2_coins_mcs_pct_t2,x.pbp_b2_coins_mcs_int_num_t2,x.pbp_b2_coins_mcs_pct_int1_t2,x.pbp_b2_coins_mcs_bgnd_int1_t2,x.pbp_b2_coins_mcs_endd_int1_t2,x.pbp_b2_coins_mcs_pct_int2_t2,x.pbp_b2_coins_mcs_bgnd_int2_t2
    ,x.pbp_b2_coins_mcs_endd_int2_t2,x.pbp_b2_coins_mcs_pct_int3_t2,x.pbp_b2_coins_mcs_bgnd_int3_t2,x.pbp_b2_coins_mcs_endd_int3_t2,x.pbp_b2_mc_copay_cstshr_yn_t2,x.pbp_b2_copay_mcs_amt_t2,x.pbp_b2_copay_mcs_int_num_t2
    ,x.pbp_b2_copay_mcs_amt_int1_t2,x.pbp_b2_copay_mcs_bgnd_int1_t2,x.pbp_b2_copay_mcs_endd_int1_t2,x.pbp_b2_copay_mcs_amt_int2_t2,x.pbp_b2_copay_mcs_bgnd_int2_t2,x.pbp_b2_copay_mcs_endd_int2_t2,x.pbp_b2_copay_mcs_amt_int3_t2
    ,x.pbp_b2_copay_mcs_bgnd_int3_t2,x.pbp_b2_copay_mcs_endd_int3_t2, x.pbp_b2_copay_ad_intrvl_num_t2, x.pbp_b2_copay_ad_amt_int1_t2, x.pbp_b2_copay_ad_bgnd_int1_t2, x.pbp_b2_copay_ad_endd_int1_t2, x.pbp_b2_ad_cost_vary_tiers_yn)
        
    @staticmethod
    def get_OON_text(x): 
        return Benefit_2().get_mc_onn_tier_benefit_text(x.pbp_c_oon_coins_snf_yn, x.pbp_c_oon_coins_snf_mc_cost_yn, x.pbp_c_oon_coins_snf_pct, x.pbp_c_oon_coins_snf_intrvl_num, 
    x.pbp_c_oon_coins_snf_pct_i1, x.pbp_c_oon_coins_snf_bgnd_i1, x.pbp_c_oon_coins_snf_endd_i1,
    x.pbp_c_oon_coins_snf_pct_i2, x.pbp_c_oon_coins_snf_bgnd_i2,x.pbp_c_oon_coins_snf_endd_i2,
    x.pbp_c_oon_coins_snf_pct_i3, x.pbp_c_oon_coins_snf_bgnd_i3,x.pbp_c_oon_coins_snf_endd_i3,
    x.pbp_c_oon_copay_snf_yn,  x.pbp_c_oon_copay_snf_mc_cost_yn, x.pbp_c_oon_copay_snf_amt,x.pbp_c_oon_copay_snf_intrvl_num,
    x.pbp_c_oon_copay_snf_amt_i1, x.pbp_c_oon_copay_snf_bgnd_i1, x.pbp_c_oon_copay_snf_endd_i1,
    x.pbp_c_oon_copay_snf_amt_i2, x.pbp_c_oon_copay_snf_bgnd_i2,x.pbp_c_oon_copay_snf_endd_i2,
    x.pbp_c_oon_copay_snf_amt_i3, x.pbp_c_oon_copay_snf_bgnd_i3,x.pbp_c_oon_copay_snf_endd_i3,
    x.pbp_c_pos_yn, x.pbp_c_pos_mc_bendesc_subcats,
    x.pbp_c_pos_coins_snf_yn, x.pbp_c_pos_coins_snf_mc_cost_yn, x.pbp_c_pos_coins_snf_intrvl_num, x.pbp_c_pos_coins_snf_pct,
    x.pbp_c_pos_coins_snf_pct_i1, x.pbp_c_pos_coins_snf_bgnd_i1, x.pbp_c_pos_coins_snf_endd_i1,
    x.pbp_c_pos_coins_snf_pct_i2, x.pbp_c_pos_coins_snf_bgnd_i2,x.pbp_c_pos_coins_snf_endd_i2,
    x.pbp_c_pos_coins_snf_pct_i3, x.pbp_c_pos_coins_snf_bgnd_i3,x.pbp_c_pos_coins_snf_endd_i3,
    x.pbp_c_pos_copay_snf_yn, x.pbp_c_pos_copay_snf_mc_cost_yn, x.pbp_c_pos_copay_snf_intrvl_num, x.pbp_c_pos_copay_snf_amt,
    x.pbp_c_pos_copay_snf_amt_i1, x.pbp_c_pos_copay_snf_bgnd_i1, x.pbp_c_pos_copay_snf_endd_i1,
    x.pbp_c_pos_copay_snf_amt_i2, x.pbp_c_pos_copay_snf_bgnd_i2,x.pbp_c_pos_copay_snf_endd_i2,
    x.pbp_c_pos_copay_snf_amt_i3, x.pbp_c_pos_copay_snf_bgnd_i3,x.pbp_c_pos_copay_snf_endd_i3)
    
class Benefit_4a(Benefit_MC):
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_4a().get_mc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                            x.pbp_b4a_coins_yn,x.pbp_b4a_coins_pct_mc_min,x.pbp_b4a_coins_pct_mc_max,
                                                            x.pbp_b4a_copay_yn,x.pbp_b4a_copay_amt_mc_min,x.pbp_b4a_copay_amt_mc_max)
        if benefit_text not in ['', '$0 copay']:
            benefit_text += ' per visit'
        return benefit_text

class Benefit_4b(Benefit_MC):
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_4b().get_mc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                            x.pbp_b4b_coins_yn,x.pbp_b4b_coins_pct_mc_min,x.pbp_b4b_coins_pct_mc_max,
                                                            x.pbp_b4b_copay_yn,x.pbp_b4b_copay_amt_mc_min,x.pbp_b4b_copay_amt_mc_max)
        if benefit_text not in ['', '$0 copay']:
            benefit_text += ' per visit'
        return benefit_text

class Benefit_7a(Benefit_MC):
    @staticmethod
    def get_INN_text(x):
        b7a = Benefit_7a()
        benefit_text = b7a.get_mc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7a_coins_yn,x.pbp_b7a_coins_pct_mc_min,x.pbp_b7a_coins_pct_mc_max,
    x.pbp_b7a_copay_yn,x.pbp_b7a_copay_amt_mc_min,x.pbp_b7a_copay_amt_mc_max)
        if benefit_text not in ['', '$0 copay']:
            benefit_text += ' per visit'
        return benefit_text
    @staticmethod
    def get_OON_text(x):
        oon_benefit_text = Benefit_MC.get_OON_text(x)
        if oon_benefit_text not in ['', '$0 copay']:
            oon_benefit_text += ' per visit'
        return oon_benefit_text

class Benefit_7b(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 2

    @staticmethod
    def get_INN_text(x):
        return Benefit_7b().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                     x.pbp_b7b_copay_yn,x.pbp_b7b_copay_ehc,x.pbp_b7b_copay_mc_amt_min, x.pbp_b7b_copay_mc_amt_max,
                                                     x.pbp_b7b_coins_yn,x.pbp_b7b_coins_ehc,x.pbp_b7b_coins_pct_mc_min,x.pbp_b7b_coins_pct_mc_max)

class Benefit_7b1(Benefit_NMC):
        
    '''
    1 in 2	Medicare-covered Chiropractic Services
    1 in 3	Routine Care
    1 in 1	Other
    '''
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 3
    
    '''
    EHC 
    1 in 2	Routine Care
    1 in 1	Other
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 2
    BENEDESC_EHC_SERVICE = 2
    
    @staticmethod
    def get_INN_text(x):
        inn_benefit_text = Benefit_7b1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                               np.nan, np.nan,
                                                               x.pbp_b7b_bendesc_yn, x.pbp_b7b_bendesc_ehc,
                                                               x.pbp_b7b_coins_yn,x.pbp_b7b_coins_ehc,x.pbp_b7b_coins_pct_rc_min,x.pbp_b7b_coins_pct_rc_max,
                                                               x.pbp_b7b_copay_yn,x.pbp_b7b_copay_ehc,x.pbp_b7b_copay_rc_amt_min,x.pbp_b7b_copay_rc_amt_max)
        if x.pbp_b7b_bendesc_lim_rc == 2:
            inn_benefit_text += f"<br/>Maximum {str(int(x.pbp_b7b_bendesc_num_rc))} {Benefit_7f_NMC().get_periodicity_text(x.pbp_b7b_bendesc_per_rc)}"
        return inn_benefit_text

class Benefit_7b2(Benefit_NMC):
        
    '''
    1 in 2	Medicare-covered Chiropractic Services
    1 in 3	Routine Care
    1 in 1	Other
    '''
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 1
    
    '''
    EHC 
    1 in 2	Routine Care
    1 in 1	Other
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 2
    BENEDESC_EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        inn_benefit_text = Benefit_7b2().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                               np.nan, np.nan,
                                                               x.pbp_b7b_bendesc_yn, x.pbp_b7b_bendesc_ehc,
                                                               x.pbp_b7b_coins_yn,x.pbp_b7b_coins_ehc,x.pbp_b7b_coins_pct_other_min, x.pbp_b7b_coins_pct_other_max,
                                                               x.pbp_b7b_copay_yn,x.pbp_b7b_copay_ehc,x.pbp_b7b_copay_other_amt_min,x.pbp_b7b_copay_other_amt_max)
        if x.pbp_b7b_bendesc_lim_other == 2:
            inn_benefit_text += f"<br/>Maximum {str(int(x.pbp_b7b_bendesc_num_other))} {Benefit_7b2().get_periodicity_text(x.pbp_b7b_bendesc_per_other)}"
        return inn_benefit_text

class Benefit_7c(Benefit_MC):    
    @staticmethod
    def get_INN_text(x):
        return  Benefit_7c().get_mc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7c_coins_yn,x.pbp_b7c_coins_pct_mc_min,x.pbp_b7c_coins_pct_mc_max,
    x.pbp_b7c_copay_yn,x.pbp_b7c_copay_mc_amt_min,x.pbp_b7c_copay_mc_amt_max)
    
class Benefit_7d(Benefit_MC):

    @staticmethod
    def get_INN_text(x):
        b7d = Benefit_7d()
        benefit_text = b7d.get_mc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                   x.pbp_b7d_coins_yn,x.pbp_b7d_coins_pct_mc_min,x.pbp_b7d_coins_pct_mc_max,
                                                   x.pbp_b7d_copay_yn,x.pbp_b7d_copay_amt_mc_min,x.pbp_b7d_copay_amt_mc_max)
        if benefit_text not in ['', '$0 copay']:
            benefit_text += ' per visit'
        return benefit_text
        
        
    @staticmethod
    def get_OON_text(x):
        oon_benefit_text = Benefit_MC.get_OON_text(x)
        if oon_benefit_text not in ['', '$0 copay']:
            oon_benefit_text += ' per visit'
        return oon_benefit_text

class Benefit_7e1(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2
    
    @staticmethod
    def get_INN_text(x):
        b8a1 = Benefit_7e1()
        return Benefit_7e1().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7e_copay_yn,x.pbp_b7e_copay_ehc,x.pbp_b7e_copay_mcis_minamt,x.pbp_b7e_copay_mcis_maxamt,
    x.pbp_b7e_coins_yn,x.pbp_b7e_coins_ehc,x.pbp_b7e_coins_mcis_minpct,x.pbp_b7e_coins_mcis_maxpct)
        
class Benefit_7e2(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        return Benefit_7e2().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7e_copay_yn,x.pbp_b7e_copay_ehc,x.pbp_b7e_copay_mcgs_minamt,x.pbp_b7e_copay_mcgs_maxamt,
    x.pbp_b7e_coins_yn,x.pbp_b7e_coins_ehc,x.pbp_b7e_coins_mcgs_minpct,x.pbp_b7e_coins_mcgs_maxpct)

class Benefit_7f(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2
    
    @staticmethod
    def get_INN_text(x):
        return Benefit_7f().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7f_copay_yn,x.pbp_b7f_copay_ehc,x.pbp_b7f_copay_mc_amt_min, x.pbp_b7f_copay_mc_amt_max,
    x.pbp_b7f_coins_yn,x.pbp_b7f_coins_ehc,x.pbp_b7f_coins_pct_mc_min, x.pbp_b7f_coins_pct_mc_max)

class Benefit_7f_NMC(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        inn_benefit_text = Benefit_7f_NMC().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7f_copay_yn,x.pbp_b7f_copay_ehc,x.pbp_b7f_copay_rf_amt_min, x.pbp_b7f_copay_rf_amt_max,
    x.pbp_b7f_coins_yn,x.pbp_b7f_coins_ehc,x.pbp_b7f_coins_pct_rf_min, x.pbp_b7f_coins_pct_rf_max)
        if x.pbp_b7f_bendesc_lim_rf  == 2:
            inn_benefit_text += f"<br/>Maximum {str(int(x.pbp_b7f_bendesc_amt_rf))} {Benefit_7f_NMC().get_periodicity_text(x.pbp_b7f_bendesc_per_rf)}"
        return inn_benefit_text

class Benefit_7h1(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2
    
    @staticmethod
    def get_INN_text(x):
        return Benefit_7h1().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7h_copay_yn,x.pbp_b7h_copay_ehc,x.pbp_b7h_copay_mcis_minamt,x.pbp_b7h_copay_mcis_maxamt,
    x.pbp_b7h_coins_yn,x.pbp_b7h_coins_ehc,x.pbp_b7h_coins_mcis_minpct,x.pbp_b7h_coins_mcis_maxpct)
        
class Benefit_7h2(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        return Benefit_7h2().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b7h_copay_yn,x.pbp_b7h_copay_ehc,x.pbp_b7h_copay_mcgs_minamt,x.pbp_b7h_copay_mcgs_maxamt,
    x.pbp_b7h_coins_yn,x.pbp_b7h_coins_ehc,x.pbp_b7h_coins_mcgs_minpct,x.pbp_b7h_coins_mcgs_maxpct)
        
class Benefit_7i(Benefit_MC):
    @staticmethod
    def get_INN_text(x):
        return Benefit_7i().get_mc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7i_coins_yn,x.pbp_b7i_coins_pct_mc_min,x.pbp_b7i_coins_pct_mc_max,
    x.pbp_b7i_copay_yn,x.pbp_b7i_copay_mc_amt_min,x.pbp_b7i_copay_mc_amt_max)

class Benefit_7j(Benefit_MC):
    @staticmethod
    def get_INN_text(x):
        return Benefit_7i().get_mc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b7j_coins_yn,x.pbp_b7j_coins_pct_mc_min,x.pbp_b7j_coins_pct_mc_max,
    x.pbp_b7j_copay_yn,x.pbp_b7j_copay_mc_amt_min,x.pbp_b7j_copay_mc_amt_max)

class Benefit_8a1(Benefit_MC_EHC):
    
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2   
    
    @staticmethod
    def get_INN_text(x):
        return Benefit_8a1().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                         x.pbp_b8a_copay_yn,x.pbp_b8a_copay_ehc,x.pbp_b8a_copay_min_dmc_amt,x.pbp_b8a_copay_max_dmc_amt,
                                                         x.pbp_b8a_coins_yn,x.pbp_b8a_coins_ehc,x.pbp_b8a_coins_pct_dmc,x.pbp_b8a_coins_pct_dmc_max)
       
class Benefit_8a2(Benefit_MC_EHC):
    
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 1    
    
    @staticmethod
    def get_INN_text(x):
        b8a2 = Benefit_8a2()
        return b8a2.get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                x.pbp_b8a_copay_yn,x.pbp_b8a_copay_ehc,x.pbp_b8a_lab_copay_amt,x.pbp_b8a_lab_copay_amt_max,
                                                x.pbp_b8a_coins_yn,x.pbp_b8a_coins_ehc,x.pbp_b8a_coins_pct_lab,x.pbp_b8a_coins_pct_lab_max)
        
class Benefit_8b1(Benefit_MC_EHC):
    
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 2
    
    @staticmethod
    def get_INN_text(x):
        b8a2 = Benefit_8b1()
        return b8a2.get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                x.pbp_b8b_copay_yn,x.pbp_b8b_copay_ehc,x.pbp_b8b_copay_amt_drs,x.pbp_b8b_copay_amt_drs_max,
                                                x.pbp_b8b_coins_yn,x.pbp_b8b_coins_ehc,x.pbp_b8b_coins_pct_drs,x.pbp_b8b_coins_pct_drs_max)
       
class Benefit_8b3(Benefit_MC_EHC):
    
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        b8a2 = Benefit_8b3()
        return b8a2.get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b8b_copay_yn,x.pbp_b8b_copay_ehc,x.pbp_b8b_copay_mc_amt,x.pbp_b8b_copay_mc_amt_max,
    x.pbp_b8b_coins_yn,x.pbp_b8b_coins_ehc,x.pbp_b8b_coins_pct_cmc,x.pbp_b8b_coins_pct_cmc_max)

class Benefit_9a1(Benefit_MC_EHC):
    '''
    EHC 
    1 in 2	Medicare-covered Outpatient Hospital Services
    1 in 1	Medicare-covered Observation Services
    '''
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2

    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_MC_EHC().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                                x.pbp_b9a_copay_yn,x.pbp_b9a_copay_ehc,x.pbp_b9a_copay_ohs_amt_min,x.pbp_b9a_copay_ohs_amt_max, 
                                                                x.pbp_b9a_coins_yn,x.pbp_b9a_coins_ehc,x.pbp_b9a_coins_ohs_pct_min,x.pbp_b9a_coins_ohs_pct_max)
        if benefit_text not in ['', '$0 copay']:
            benefit_text += ' per visit'
        return benefit_text
    
    @staticmethod
    def get_OON_text(x): 
        oon_benefit_text = Benefit_MC_EHC().get_oon_benefit_text(x.pbp_c_oon_yn, 
    x.pbp_c_oon_outpt_coins_yn,x.pbp_c_oon_outpt_coins_min_pct,x.pbp_c_oon_outpt_coins_max_pct,
    x.pbp_c_oon_outpt_copay_yn,x.pbp_c_oon_outpt_copay_min_amt,x.pbp_c_oon_outpt_copay_max_amt,
    x.pbp_c_pos_outpt_coins_yn,x.pbp_c_pos_outpt_coins_min_pct,x.pbp_c_pos_outpt_coins_max_pct,
    x.pbp_c_pos_outpt_copay_yn,x.pbp_c_pos_outpt_copay_min_amt,x.pbp_c_pos_outpt_copay_max_amt)
        if oon_benefit_text not in ['', '$0 copay']:
            oon_benefit_text += ' per visit'
        return oon_benefit_text

class Benefit_10a1(Benefit_MC_EHC):
    
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2
    @staticmethod
    def get_INN_text(x):
        return Benefit_10a1().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b10a_copay_yn,x.pbp_b10a_copay_ehc,x.pbp_b10a_copay_gas_amt_min,x.pbp_b10a_copay_gas_amt_max,
    x.pbp_b10a_coins_yn,x.pbp_b10a_coins_ehc,x.pbp_b10a_coins_gas_pct_min,x.pbp_b10a_coins_gas_pct_max)

class Benefit_10a2(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 1
    def get_INN_text(x):
        return Benefit_10a2().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b10a_copay_yn,x.pbp_b10a_copay_ehc,x.pbp_b10a_copay_aas_amt_min,x.pbp_b10a_copay_aas_amt_max,
    x.pbp_b10a_coins_yn,x.pbp_b10a_coins_ehc,x.pbp_b10a_coins_aas_pct_min,x.pbp_b10a_coins_aas_pct_max)

class Benefit_10b1(Benefit_NMC):
        
    EHC_TOTAL_SERVICE = np.nan
    EHC_SERVICE = np.nan

    BENEDESC_EHC_TOTAL_SERVICE = np.nan
    BENEDESC_EHC_SERVICE = np.nan
    
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_10b1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    np.nan, np.nan, x.pbp_b10b_bendesc_yn, x.pbp_b10b_bendesc_trn,
    x.pbp_b10b_coins_yn,np.nan,x.pbp_b10b_coins_pct_min,x.pbp_b10b_coins_pct_max,
    x.pbp_b10b_copay_yn,np.nan,x.pbp_b10b_copay_amt_min,x.pbp_b10b_copay_amt_max)
        if x.pbp_b10b_bendesc_tt_pal == 1:
            benefit_text += '<br/>'
            if x.pbp_b10b_bendesc_lim_pal == 1:
                benefit_text += 'Plan allows one way trips to a plan-approved location.'
            elif x.pbp_b10b_bendesc_lim_pal == 2:
                benefit_text += f"Plan allows {str(int(x.pbp_b10b_bendesc_amt_pal))} one way trips to a plan-approved location {Benefit_10b1().get_periodicity_text(x.pbp_b10b_bendesc_per_pal)}."
        elif x.pbp_b10b_bendesc_tt_pal == 5:
            benefit_text += '<br/>'
            if x.pbp_b10b_bendesc_lim_pal == 1:
                benefit_text += 'Plan allows one way trips to a plan-approved location - See EOC for details..'
            elif x.pbp_b10b_bendesc_lim_pal == 2:
                benefit_text += f"Plan allows {str(int(x.pbp_b10b_bendesc_amt_pal))} one way trips to a plan-approved location {Benefit_10b1().get_periodicity_text(x.pbp_b10b_bendesc_per_pal)} - See EOC for details.."
        
        return benefit_text

class Benefit_11a(Benefit_MC):
    @staticmethod
    def get_INN_text(x):
        inn_benefit = Benefit_11a().get_mc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                            x.pbp_b11a_coins_yn,x.pbp_b11a_coins_pct_mc,x.pbp_b11a_coins_pct_mcmax,
                                                            x.pbp_b11a_copay_yn,x.pbp_b11a_copay_mc_amt,x.pbp_b11a_copay_mcmax_amt)
        if inn_benefit not in (['$0 copay']):
            inn_benefit = inn_benefit + ' per item'
        return inn_benefit
    
    @staticmethod
    def get_OON_text(x): 
        oon_benefit_text = Benefit_MC.get_OON_text(x)
        if oon_benefit_text not in ['', '$0 copay']:
            oon_benefit_text += ' per item'
        return oon_benefit_text
        
class Benefit_11b1(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2
    '''
    1 in 2	Medicare-covered Prosthetic Devices
    1 in 1	Medicare-covered Medical Supplies
    '''
    @staticmethod
    def get_INN_text(x):
        inn_benefit = Benefit_11b1().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b11b_copay_yn,x.pbp_b11b_copay_ehc,x.pbp_b11b_copay_mcmin_amt, x.pbp_b11b_copay_mcmax_amt,
    x.pbp_b11b_coins_yn,x.pbp_b11b_coins_ehc,x.pbp_b11b_coins_pct_mc,x.pbp_b11b_coins_pct_mcmax)
        if inn_benefit not in (['$0 copay']):
            inn_benefit = inn_benefit + ' per item'
        return inn_benefit
        
        
    @staticmethod
    def get_OON_text(x): 
        oon_benefit_text = Benefit_MC_EHC.get_OON_text(x)
        if oon_benefit_text not in ['', '$0 copay']:
            oon_benefit_text += ' per item'
        return oon_benefit_text
        
class Benefit_11c1(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2
    '''    
    1 in 2	Medicare-covered Diabetes Supplies
    1 in 1	Medicare-covered Diabetic Therapeutic Shoes or Inserts
    '''
    @staticmethod
    def get_INN_text(x):
        inn_benefit = Benefit_11c1().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    x.pbp_b11c_copay_yn,x.pbp_b11c_copay_ehc,x.pbp_b11c_copay_mcmin_amt,x.pbp_b11c_copay_mcmax_amt,
    x.pbp_b11c_coins_yn,x.pbp_b11c_coins_ehc,x.pbp_b11c_coins_pct_mcmin,x.pbp_b11c_coins_pct_mcmax)
        if inn_benefit not in (['$0 copay']):
            inn_benefit = inn_benefit + ' per item'
        return inn_benefit
        
    @staticmethod
    def get_OON_text(x): 
        oon_benefit_text = Benefit_MC_EHC.get_OON_text(x)
        if oon_benefit_text not in ['', '$0 copay']:
            oon_benefit_text += ' per item'
        return oon_benefit_text

class Benefit_13a(Benefit_NMC):
        
    EHC_TOTAL_SERVICE = np.nan
    EHC_SERVICE = np.nan

    '''
    1 in 1	Number of Treatments
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 1
    BENEDESC_EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_13a().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    np.nan, np.nan,
    x.pbp_b13a_bendesc_yn, x.pbp_b13a_bendesc_ehc,
    x.pbp_b13a_coins_yn,np.nan,x.pbp_b13a_coins_pct_min,x.pbp_b13a_coins_pct_max,
    x.pbp_b13a_copay_yn,np.nan,x.pbp_b13a_copay_amt_min,x.pbp_b13a_copay_amt_max)
        if x.pbp_b13a_bendesc_lim == 2:
            benefit_text += f"<br/>Maximum {str(int(x.pbp_b13a_bendesc_numv))} {Benefit_13a().get_periodicity_text(x.pbp_b13a_bendesc_per)}"
        return benefit_text

class Benefit_13b(Benefit_NMC):
        
    EHC_TOTAL_SERVICE = np.nan
    EHC_SERVICE = np.nan

    BENEDESC_EHC_TOTAL_SERVICE = np.nan
    BENEDESC_EHC_SERVICE = np.nan
    
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_13b().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    np.nan, np.nan,
    np.nan, np.nan,
    x.pbp_b13b_coins_yn,np.nan,x.pbp_b13b_coins_pct_min,x.pbp_b13b_coins_pct_max,
    x.pbp_b13b_copay_yn,np.nan,x.pbp_b13b_copay_amt_min,x.pbp_b13b_copay_amt_max)
        if x.pbp_b13b_maxplan_yn == 1:
            benefit_text += f"<br/>Maximum ${str(int(x.pbp_b13b_maxplan_amt))} {Benefit_13b().get_periodicity_text(x.pbp_b13b_otc_maxplan_per)}"
        return benefit_text

class Benefit_13c(Benefit_NMC):
        
    EHC_TOTAL_SERVICE = np.nan
    EHC_SERVICE = np.nan

    BENEDESC_EHC_TOTAL_SERVICE = np.nan
    BENEDESC_EHC_SERVICE = np.nan
    
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_13c().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
    np.nan, np.nan,
    np.nan, np.nan,
    x.pbp_b13c_coins_yn,np.nan,x.pbp_b13c_coins_pct_min,x.pbp_b13c_coins_pct_max,
    x.pbp_b13c_copay_yn,np.nan,x.pbp_b13c_copay_amt_min,x.pbp_b13c_copay_amt_max)
        if x.pbp_b13c_maxplan_yn == 1:
            benefit_text += f"<br/>Maximum ${str(int(x.pbp_b13c_maxplan_amt))} {Benefit_13c().get_periodicity_text(x.pbp_b13c_maxplan_per)}"
        return benefit_text

class Benefit_14a(Benefit_MC):
    
    EHC_TOTAL_SERVICE = np.nan
    EHC_SERVICE = np.nan
    
    def get_14a_inn_benefit_text(self, pbp_b14a_mc_prevent_attest):
        if pbp_b14a_mc_prevent_attest == 1:
            return '$0 copay'
        return 'Not covered'

    @staticmethod
    def get_INN_text(x):
        b14a = Benefit_14a()
        benefit_text = b14a.get_14a_inn_benefit_text(x.pbp_b14a_mc_prevent_attest)
        return benefit_text

class Benefit_14c4(Benefit_NMC):
    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    EHC_TOTAL_SERVICE = 1
    EHC_SERVICE = 1

    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 1
    BENEDESC_EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        bendesc_ehc = np.nan
        coins_ehc = np.nan
        copay_ehc = np.nan
        if x.pbp_b14c_bendesc_yn == 1 and isinstance(x.pbp_b14c_bendesc_ehc, str):
            if '14c4;' in x.pbp_b14c_bendesc_ehc + ';':
                bendesc_ehc = 1
            else:
                bendesc_ehc = 0
        if x.pbp_b14c_coins_yn == 1 and isinstance(x.pbp_b14c_coins_ehc, str):
            if '14c4;' in x.pbp_b14c_coins_ehc + ';':
                coins_ehc = 1
            else:
                coins_ehc = 0
        if x.pbp_b14c_copay_yn == 1 and isinstance(x.pbp_b14c_copay_ehc, str):
            if '14c4;' in x.pbp_b14c_copay_ehc + ';':
                copay_ehc = 1
            else:
                copay_ehc = 0
        benefit_text = Benefit_14c4().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                               np.nan, np.nan, 
                                                               x.pbp_b14c_bendesc_yn, bendesc_ehc, 
                                                               x.pbp_b14c_coins_yn,coins_ehc,x.pbp_b14c_coins_pct_min_mhc, x.pbp_b14c_coins_pct_max_mhc,
                                                               x.pbp_b14c_copay_yn,copay_ehc,x.pbp_b14c_copay_mhc_min_amt,x.pbp_b14c_copay_mhc_max_amt)
        return benefit_text

class Benefit_14c7(Benefit_NMC):
    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    EHC_TOTAL_SERVICE = 1
    EHC_SERVICE = 1

    '''
    1 in 2	Web/Phone-based technologies
    1 in 1	Nursing Hotline
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 2
    BENEDESC_EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        coins_ehc = np.nan
        copay_ehc = np.nan

        if x.pbp_b14c_coins_yn == 1 and isinstance(x.pbp_b14c_coins_ehc, str):
            if '14c7;' in x.pbp_b14c_coins_ehc + ';':
                coins_ehc = 1
            else:
                coins_ehc = 0
        if x.pbp_b14c_copay_yn == 1 and isinstance(x.pbp_b14c_copay_ehc, str):
            if '14c7;' in x.pbp_b14c_copay_ehc + ';':
                copay_ehc = 1
            else:
                copay_ehc = 0
        benefit_text = Benefit_14c7().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                               np.nan, np.nan, 
                                                               x.pbp_b14c_bendesc_yn, x.pbp_b14c_rat_bendesc_ehc, 
                                                               x.pbp_b14c_coins_yn,coins_ehc,x.pbp_b14c_coins_pct_min_rat_nh,x.pbp_b14c_coins_pct_max_rat_nh,
                                                               x.pbp_b14c_copay_yn,copay_ehc,x.pbp_b14c_copay_rat_nh_min_amt,x.pbp_b14c_copay_rat_nh_max_amt)
        return benefit_text

class Benefit_14c10(Benefit_NMC):
    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    EHC_TOTAL_SERVICE = 1
    EHC_SERVICE = 1

    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 1
    BENEDESC_EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        coins_ehc = np.nan
        copay_ehc = np.nan
        bendesc_ehc = np.nan
        if x.pbp_b14c_bendesc_yn == 1 and isinstance(x.pbp_b14c_bendesc_ehc, str):
            if '14c10;' in x.pbp_b14c_bendesc_ehc + ';':
                bendesc_ehc = 1
            else:
                bendesc_ehc = 0
        if x.pbp_b14c_coins_yn == 1 and isinstance(x.pbp_b14c_coins_ehc, str):
            if '14c10;' in x.pbp_b14c_coins_ehc + ';':
                coins_ehc = 1
            else:
                coins_ehc = 0
        if x.pbp_b14c_copay_yn == 1 and isinstance(x.pbp_b14c_copay_ehc, str):
            if '14c10;' in x.pbp_b14c_copay_ehc + ';':
                copay_ehc = 1
            else:
                copay_ehc = 0
        benefit_text = Benefit_14c10().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                               np.nan, np.nan, 
                                                               x.pbp_b14c_bendesc_yn, bendesc_ehc,
                                                               x.pbp_b14c_coins_yn,coins_ehc,x.pbp_b14c_coins_pct_min_isa, x.pbp_b14c_coins_pct_max_isa,
                                                               x.pbp_b14c_copay_yn,copay_ehc,x.pbp_b14c_copay_isa_min_amt, x.pbp_b14c_copay_isa_max_amt)
        return benefit_text

class Benefit_14c11(Benefit_NMC):
    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    EHC_TOTAL_SERVICE = 1
    EHC_SERVICE = 1

    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 1
    BENEDESC_EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        coins_ehc = np.nan
        copay_ehc = np.nan
        bendesc_ehc = np.nan
        if x.pbp_b14c_bendesc_yn == 1 and isinstance(x.pbp_b14c_bendesc_ehc, str):
            if '14c11;' in x.pbp_b14c_bendesc_ehc + ';':
                bendesc_ehc = 1
            else:
                bendesc_ehc = 0
        if x.pbp_b14c_coins_yn == 1 and isinstance(x.pbp_b14c_coins_ehc, str):
            if '14c11;' in x.pbp_b14c_coins_ehc + ';':
                coins_ehc = 1
            else:
                coins_ehc = 0
        if x.pbp_b14c_copay_yn == 1 and isinstance(x.pbp_b14c_copay_ehc, str):
            if '14c11;' in x.pbp_b14c_copay_ehc + ';':
                copay_ehc = 1
            else:
                copay_ehc = 0
        benefit_text = Benefit_14c10().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                               np.nan, np.nan, 
                                                               x.pbp_b14c_bendesc_yn, bendesc_ehc,
                                                               x.pbp_b14c_coins_yn,coins_ehc,x.pbp_b14c_coins_pct_min_prs, x.pbp_b14c_coins_pct_max_prs,
                                                               x.pbp_b14c_copay_yn,copay_ehc,x.pbp_b14c_copay_prs_min_amt, x.pbp_b14c_copay_prs_max_amt)
        return benefit_text

class Benefit_14c21(Benefit_NMC):
    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    EHC_TOTAL_SERVICE = 1
    EHC_SERVICE = 1


    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 1
    BENEDESC_EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        coins_ehc = np.nan
        copay_ehc = np.nan
        bendesc_ehc = np.nan

        if x.pbp_b14c_bendesc_yn == 1 and isinstance(x.pbp_b14c_bendesc_ehc, str):
            if '14c21;' in x.pbp_b14c_bendesc_ehc + ';':
                bendesc_ehc = 1
            else:
                bendesc_ehc = 0
        if x.pbp_b14c_coins_yn == 1 and isinstance(x.pbp_b14c_coins_ehc, str):
            if '14c21;' in x.pbp_b14c_coins_ehc + ';':
                coins_ehc = 1
            else:
                coins_ehc = 0
        if x.pbp_b14c_copay_yn == 1 and isinstance(x.pbp_b14c_copay_ehc, str):
            if '14c21;' in x.pbp_b14c_copay_ehc + ';':
                copay_ehc = 1
            else:
                copay_ehc = 0
        benefit_text = Benefit_14c21().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                               np.nan, np.nan, 
                                                               x.pbp_b14c_bendesc_yn, bendesc_ehc,
                                                               x.pbp_b14c_coins_yn,coins_ehc,x.pbp_b14c_coins_pct_min_ihss,x.pbp_b14c_coins_pct_max_ihss,
                                                               x.pbp_b14c_copay_yn,copay_ehc,x.pbp_b14c_copay_min_amt_ihss, x.pbp_b14c_copay_max_amt_ihss)
        return benefit_text


class Benefit_14c22(Benefit_NMC):
    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    EHC_TOTAL_SERVICE = 1
    EHC_SERVICE = 1


    
    '''
    14c1	14c1: Health Education
14c10	14c10: In-Home Safety Assessment
14c11	14c11: Personal Emergency Response System (PERS)
14c12	14c12: Medical Nutrition Therapy (MNT)
14c13	14c13: Post discharge In-Home Medication Reconciliation
14c14	14c14: Re-admission Prevention
14c15	14c15: Wigs for Hair Loss Related to Chemotherapy
14c16	14c16: Weight Management Programs*
14c17	14c17: Alternative Therapies*
14c18	14c18: Therapeutic Massage
14c19	14c19: Adult Day Health Services
14c2	14c2: Nutritional/Dietary Benefit
14c20	14c20: Home-Based Palliative Care
14c21	14c21: In-Home Support Services
14c22	14c22: Support for Caregivers of Enrollees
14c3	14c3: Additional Sessions of Smoking and Tobacco Cessation Counseling
14c4	14c4: Fitness Benefit*
14c5	14c5: Enhanced Disease Management
14c6	14c6: Telemonitoring Services*
14c7	14c7: Remote Access Technologies (including Web/Phone-based technologies and Nursing Hotline)*
14c8	14c8: Home and Bathroom Safety Devices and Modifications*
14c9	14c9: Counseling Services
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 1
    BENEDESC_EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        coins_ehc = np.nan
        copay_ehc = np.nan
        bendesc_ehc = np.nan

        if x.pbp_b14c_bendesc_yn == 1 and isinstance(x.pbp_b14c_bendesc_ehc, str):
            if '14c22;' in x.pbp_b14c_bendesc_ehc + ';':
                bendesc_ehc = 1
            else:
                bendesc_ehc = 0
        if x.pbp_b14c_coins_yn == 1 and isinstance(x.pbp_b14c_coins_ehc, str):
            if '14c22;' in x.pbp_b14c_coins_ehc + ';':
                coins_ehc = 1
            else:
                coins_ehc = 0
        if x.pbp_b14c_copay_yn == 1 and isinstance(x.pbp_b14c_copay_ehc, str):
            if '14c22;' in x.pbp_b14c_copay_ehc + ';':
                copay_ehc = 1
            else:
                copay_ehc = 0
        benefit_text = Benefit_14c22().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                               np.nan, np.nan, 
                                                               x.pbp_b14c_bendesc_yn, bendesc_ehc,
                                                               x.pbp_b14c_coins_yn,coins_ehc,x.pbp_b14c_coins_pct_min_sce,x.pbp_b14c_coins_pct_max_sce,
                                                               x.pbp_b14c_copay_yn,copay_ehc,x.pbp_b14c_copay_min_amt_sce, x.pbp_b14c_copay_max_amt_sce)
        return benefit_text


class Benefit_15_1_I(Benefit_MC):
    @staticmethod
    def get_INN_text(x):
        b15_1_i = Benefit_15_1_I()
        inn_benefit = b15_1_i.get_mc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                    x.mrx_b_ira_coins_yn,x.mrx_b_ira_coins_min_pct,x.mrx_b_ira_coins_max_pct,
                                                    x.mrx_b_ira_copay_yn,x.mrx_b_ira_copay_amt_min,x.mrx_b_ira_copay_amt_max)
        if not np.isnan(x.mrx_b_ira_copay_month_amt) and inn_benefit not in ('$0 copay') and not inn_benefit.startswith('$0 copay or '):
            inn_benefit += f' (up to {b15_1_i.convert_to_currency_no_decimal(x.mrx_b_ira_copay_month_amt)})'
        return inn_benefit

class Benefit_15_2(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 2
    
    @staticmethod
    def get_INN_text(x):
        b15_2 = Benefit_15_2()
        return b15_2.get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                 x.mrx_b_copay_yn,x.mrx_b_copay_ehc,x.mrx_b_chemo_copay_amt_min,x.mrx_b_chemo_copay_amt_max,
                                                 x.mrx_b_coins_yn,x.mrx_b_coins_ehc,x.mrx_b_chemo_coins_min_pct,x.mrx_b_chemo_coins_max_pct)
        
class Benefit_15_3(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 2
    EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        b15_3 = Benefit_15_3()
        return b15_3.get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                                 x.mrx_b_copay_yn,x.mrx_b_copay_ehc,x.mrx_b_copay_min_amt,x.mrx_b_copay_max_amt,
                                                 x.mrx_b_coins_yn,x.mrx_b_coins_ehc,x.mrx_b_coins_min_pct,x.mrx_b_coins_max_pct)
        
class Benefit_16a1(Benefit_NMC):
        
    '''
    EHC 
    1 in 2	Oral Exams
    1 in 3	Prophylaxis (Cleaning)
    1 in 4	Fluoride Treatment
    1 in 1	Dental X-Rays
    '''
    EHC_TOTAL_SERVICE = 4
    EHC_SERVICE = 2

    
    BENEDESC_EHC_TOTAL_SERVICE = 4
    BENEDESC_EHC_SERVICE = 2
    
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_16a1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b16a_copay_cserv_sc_pov_yn,x.pbp_b16a_coins_cserv_sc_pov_yn, 
    x.pbp_b16a_bendesc_yn, x.pbp_b16a_bendesc_ehc,
    x.pbp_b16a_coins_yn,x.pbp_b16a_coins_ehc,x.pbp_b16a_coins_pct_oe,x.pbp_b16a_coins_pct_maxoe,
    x.pbp_b16a_copay_yn,x.pbp_b16a_copay_ehc,x.pbp_b16a_copay_amt_oemin,x.pbp_b16a_copay_amt_oemax)
        if benefit_text not in ['', '$0 copay', 'Covered under office visit', 'Not covered']:
            benefit_text += ' per visit'
        return benefit_text

class Benefit_16a2(Benefit_NMC):
    '''
    EHC 
    1 in 2	Oral Exams
    1 in 3	Prophylaxis (Cleaning)
    1 in 4	Fluoride Treatment
    1 in 1	Dental X-Rays
    '''
    EHC_TOTAL_SERVICE = 4
    EHC_SERVICE = 3
    BENEDESC_EHC_TOTAL_SERVICE = 4
    BENEDESC_EHC_SERVICE = 3

    @staticmethod
    def get_INN_text(x):
        b16a2 = Benefit_16a2()
        return b16a2.get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b16a_copay_cserv_sc_pov_yn,x.pbp_b16a_coins_cserv_sc_pov_yn, 
    x.pbp_b16a_bendesc_yn, x.pbp_b16a_bendesc_ehc,
    x.pbp_b16a_coins_yn,x.pbp_b16a_coins_ehc,x.pbp_b16a_coins_pct_pc,x.pbp_b16a_coins_pct_maxpc,
    x.pbp_b16a_copay_yn,x.pbp_b16a_copay_ehc,x.pbp_b16a_copay_amt_pcmin,x.pbp_b16a_copay_amt_pcmax)
        
class Benefit_16a3(Benefit_NMC):
    '''
    EHC 
    1 in 2	Oral Exams
    1 in 3	Prophylaxis (Cleaning)
    1 in 4	Fluoride Treatment
    1 in 1	Dental X-Rays
    '''
    EHC_TOTAL_SERVICE = 4
    EHC_SERVICE = 4
    BENEDESC_EHC_TOTAL_SERVICE = 4
    BENEDESC_EHC_SERVICE = 4

    @staticmethod
    def get_INN_text(x):
        b16a3 = Benefit_16a3()
        
        return b16a3.get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b16a_copay_cserv_sc_pov_yn,x.pbp_b16a_coins_cserv_sc_pov_yn, 
    x.pbp_b16a_bendesc_yn, x.pbp_b16a_bendesc_ehc,
    x.pbp_b16a_coins_yn,x.pbp_b16a_coins_ehc,x.pbp_b16a_coins_pct_ft,x.pbp_b16a_coins_pct_maxft, 
    x.pbp_b16a_copay_yn,x.pbp_b16a_copay_ehc,x.pbp_b16a_copay_amt_ftmin,x.pbp_b16a_copay_amt_ftmax)
          
class Benefit_16a4(Benefit_NMC):
    '''
    EHC 
    1 in 2	Oral Exams
    1 in 3	Prophylaxis (Cleaning)
    1 in 4	Fluoride Treatment
    1 in 1	Dental X-Rays
    '''
    EHC_TOTAL_SERVICE = 4
    EHC_SERVICE = 1
    BENEDESC_EHC_TOTAL_SERVICE = 4
    BENEDESC_EHC_SERVICE = 1

    @staticmethod
    def get_INN_text(x):
        return Benefit_16a4().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
    x.pbp_b16a_copay_cserv_sc_pov_yn,x.pbp_b16a_coins_cserv_sc_pov_yn, 
    x.pbp_b16a_bendesc_yn, x.pbp_b16a_bendesc_ehc,
    x.pbp_b16a_coins_yn,x.pbp_b16a_coins_ehc,x.pbp_b16a_coins_pct_dx,x.pbp_b16a_coins_pct_maxdx, 
    x.pbp_b16a_copay_yn,x.pbp_b16a_copay_ehc,x.pbp_b16a_copay_amt_dxmin,x.pbp_b16a_copay_amt_dxmax)

class Benefit_16b1(Benefit_NMC):
        
    '''
    EHC 
    1 in 2	Dental X-Rays
    1 in 3	Other Diagnostic Dental Services
    1 in 4	Prophylaxis (Cleaning)
    1 in 5	Fluoride Treatment
    1 in 6	Other Preventive Dental Services
    1 in 1	Oral Exams
    '''
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 1

    
    BENEDESC_EHC_TOTAL_SERVICE = 6
    BENEDESC_EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        try:
            coins_ehc = 111111
            copay_ehc = 111111
            if x.pbp_b16b_coins_ov_yn == 1:
                x.pbp_b16b_coins_oe_yn = 1
                coins_ehc = x.pbp_b16b_coins_ov_svcs
                x.pbp_b16b_coins_ov_yn = 2

            if x.pbp_b16b_copay_ov_yn == 1:
                x.pbp_b16b_copay_oe_yn = 1
                copay_ehc = x.pbp_b16b_copay_ov_svcs
                x.pbp_b16b_copay_ov_yn = 2
            
            benefit_text = Benefit_16b1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
            x.pbp_b16b_copay_ov_yn,x.pbp_b16b_coins_ov_yn, 
            np.nan, np.nan,
            x.pbp_b16b_coins_oe_yn,coins_ehc,x.pbp_b16b_coins_oe_pct_min,x.pbp_b16b_coins_oe_pct_max,
            x.pbp_b16b_copay_oe_yn,copay_ehc,x.pbp_b16b_copay_oe_amt_min,x.pbp_b16b_copay_oe_amt_max)
            if benefit_text not in ['', '$0 copay', 'Covered under office visit', 'Not covered']:
                benefit_text += ' per visit'
        except:
            benefit_text = 'ERROR'
        return benefit_text
class Benefit_16b2(Benefit_NMC):
        
    '''
    EHC 
    1 in 2	Dental X-Rays
    1 in 3	Other Diagnostic Dental Services
    1 in 4	Prophylaxis (Cleaning)
    1 in 5	Fluoride Treatment
    1 in 6	Other Preventive Dental Services
    1 in 1	Oral Exams
    '''
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 2

    
    BENEDESC_EHC_TOTAL_SERVICE = 6
    BENEDESC_EHC_SERVICE = 2
    
    @staticmethod
    def get_INN_text(x):
        try:
            coins_ehc = 111111
            copay_ehc = 111111
            if x.pbp_b16b_coins_ov_yn == 1:
                x.pbp_b16b_coins_oe_yn = 1
                coins_ehc = x.pbp_b16b_coins_ov_svcs
                x.pbp_b16b_coins_ov_yn = 2

            if x.pbp_b16b_copay_ov_yn == 1:
                x.pbp_b16b_copay_oe_yn = 1
                copay_ehc = x.pbp_b16b_copay_ov_svcs
                x.pbp_b16b_copay_ov_yn = 2
            
            benefit_text = Benefit_16b1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
            x.pbp_b16b_copay_ov_yn,x.pbp_b16b_coins_ov_yn, 
            np.nan, np.nan,
            x.pbp_b16b_coins_dx_yn,coins_ehc,x.pbp_b16b_coins_dx_pct_min,x.pbp_b16b_coins_dx_pct_max,
            x.pbp_b16b_copay_dx_yn,copay_ehc,x.pbp_b16b_copay_dx_amt_min,x.pbp_b16b_copay_dx_amt_max)
            if benefit_text not in ['', '$0 copay', 'Covered under office visit', 'Not covered']:
                benefit_text += ' per visit'
        except:
            benefit_text = 'ERROR'
        return benefit_text

class Benefit_16b4(Benefit_NMC):
        
    '''
    EHC 
    1 in 2	Dental X-Rays
    1 in 3	Other Diagnostic Dental Services
    1 in 4	Prophylaxis (Cleaning)
    1 in 5	Fluoride Treatment
    1 in 6	Other Preventive Dental Services
    1 in 1	Oral Exams
    '''
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 4

    
    BENEDESC_EHC_TOTAL_SERVICE = 6
    BENEDESC_EHC_SERVICE = 4
    
    @staticmethod
    def get_INN_text(x):
        try:
            coins_ehc = 111111
            copay_ehc = 111111
            if x.pbp_b16b_coins_ov_yn == 1:
                x.pbp_b16b_coins_oe_yn = 1
                coins_ehc = x.pbp_b16b_coins_ov_svcs
                x.pbp_b16b_coins_ov_yn = 2

            if x.pbp_b16b_copay_ov_yn == 1:
                x.pbp_b16b_copay_oe_yn = 1
                copay_ehc = x.pbp_b16b_copay_ov_svcs
                x.pbp_b16b_copay_ov_yn = 2
            
            benefit_text = Benefit_16b4().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
            x.pbp_b16b_copay_ov_yn,x.pbp_b16b_coins_ov_yn, 
            np.nan, np.nan,
            x.pbp_b16b_coins_pc_yn,coins_ehc,x.pbp_b16b_coins_pc_pct_min,x.pbp_b16b_coins_pc_pct_max,
            x.pbp_b16b_copay_pc_yn,copay_ehc,x.pbp_b16b_copay_pc_amt_min,x.pbp_b16b_copay_pc_amt_max)
            if benefit_text not in ['', '$0 copay', 'Covered under office visit', 'Not covered']:
                benefit_text += ' per visit'
        except:
            benefit_text = 'ERROR'
        return benefit_text

class Benefit_16b5(Benefit_NMC):
        
    '''
    EHC 
    1 in 2	Dental X-Rays
    1 in 3	Other Diagnostic Dental Services
    1 in 4	Prophylaxis (Cleaning)
    1 in 5	Fluoride Treatment
    1 in 6	Other Preventive Dental Services
    1 in 1	Oral Exams
    '''
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 5

    
    BENEDESC_EHC_TOTAL_SERVICE = 6
    BENEDESC_EHC_SERVICE = 5
    
    @staticmethod
    def get_INN_text(x):
        try:
            coins_ehc = 111111
            copay_ehc = 111111
            if x.pbp_b16b_coins_ov_yn == 1:
                x.pbp_b16b_coins_oe_yn = 1
                coins_ehc = x.pbp_b16b_coins_ov_svcs
                x.pbp_b16b_coins_ov_yn = 2

            if x.pbp_b16b_copay_ov_yn == 1:
                x.pbp_b16b_copay_oe_yn = 1
                copay_ehc = x.pbp_b16b_copay_ov_svcs
                x.pbp_b16b_copay_ov_yn = 2
            
            benefit_text = Benefit_16b4().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
            x.pbp_b16b_copay_ov_yn,x.pbp_b16b_coins_ov_yn, 
            np.nan, np.nan,
            x.pbp_b16b_coins_ft_yn,coins_ehc,x.pbp_b16b_coins_ft_pct_min,x.pbp_b16b_coins_ft_pct_max,
            x.pbp_b16b_copay_ft_yn,copay_ehc,x.pbp_b16b_copay_ft_amt_min,x.pbp_b16b_copay_ft_amt_max)
            if benefit_text not in ['', '$0 copay', 'Covered under office visit', 'Not covered']:
                benefit_text += ' per visit'
        except:
            benefit_text = 'ERROR'
        return benefit_text

        
class Benefit_17a1(Benefit_NMC):
    '''
    1 in 2	Routine Eye Exams
    1 in 1	Other
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 2
    BENEDESC_EHC_SERVICE = 2
    '''
    1 in 2	Medicare-covered Benefits
    1 in 3	Routine Eye Exams
    1 in 1	Other
    '''
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 3
        
    @staticmethod
    def get_INN_text(x):
        return Benefit_17a1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                              np.nan, np.nan, 
                                             x.pbp_b17a_bendesc_yn, x.pbp_b17a_bendesc_ehc,
    x.pbp_b17a_coins_yn,x.pbp_b17a_coins_ehc,x.pbp_b17a_coins_pct_rex_min, x.pbp_b17a_coins_pct_rex_max,
    x.pbp_b17a_copay_yn,x.pbp_b17a_copay_ehc,x.pbp_b17a_copay_amt_rex_min, x.pbp_b17a_copay_amt_rex_max)
    
class Benefit_17b(Benefit_MC_EHC):
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 2

    @staticmethod
    def get_INN_text(x):
        inn_benefit = Benefit_17b().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc, x.pbp_b17b_copay_amt_mc_min, x.pbp_b17b_copay_amt_mc_max,
                                                    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc, x.pbp_b17b_coins_pct_mc_min, x.pbp_b17b_coins_pct_mc_max)
        return inn_benefit

class Benefit_17b1(Benefit_NMC):
    '''
    1 in 2	Contact lenses
    1 in 3	Eyeglasses (lenses and frames)
    1 in 4	Eyeglass lenses
    1 in 5	Eyeglass frames
    1 in 1	Upgrades
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 5
    BENEDESC_EHC_SERVICE = 2
    '''
    1 in 2	Medicare-covered Benefits
    1 in 3	Contact lenses
    1 in 4	Eyeglasses (lenses and frames)
    1 in 5	Eyeglass lenses
    1 in 6	Eyeglass frames
    1 in 1	Upgrades
    '''
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 3
    
    @staticmethod
    def get_INN_text(x):
        b17b1 = Benefit_17b1()
        return b17b1.get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                              np.nan, np.nan, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_cl_min,x.pbp_b17b_coins_pct_cl_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_cl_min,x.pbp_b17b_copay_amt_cl_max)
        
class Benefit_17b2(Benefit_NMC):
    '''
    1 in 2	Contact lenses
    1 in 3	Eyeglasses (lenses and frames)
    1 in 4	Eyeglass lenses
    1 in 5	Eyeglass frames
    1 in 1	Upgrades
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 5
    BENEDESC_EHC_SERVICE = 3
    '''
    1 in 2	Medicare-covered Benefits
    1 in 3	Contact lenses
    1 in 4	Eyeglasses (lenses and frames)
    1 in 5	Eyeglass lenses
    1 in 6	Eyeglass frames
    1 in 1	Upgrades
    '''
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 4
    
    @staticmethod
    def get_INN_text(x):
        b17b1 = Benefit_17b2()
        return b17b1.get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                              np.nan, np.nan, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_egs_min, x.pbp_b17b_coins_pct_egs_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_egs_min, x.pbp_b17b_copay_amt_egs_max)
        
class Benefit_17b3(Benefit_NMC):
    '''
    1 in 2	Contact lenses
    1 in 3	Eyeglasses (lenses and frames)
    1 in 4	Eyeglass lenses
    1 in 5	Eyeglass frames
    1 in 1	Upgrades
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 5
    BENEDESC_EHC_SERVICE = 4
    '''
    1 in 2	Medicare-covered Benefits
    1 in 3	Contact lenses
    1 in 4	Eyeglasses (lenses and frames)
    1 in 5	Eyeglass lenses
    1 in 6	Eyeglass frames
    1 in 1	Upgrades
    '''
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 5
    
    @staticmethod
    def get_INN_text(x):
        b17b1 = Benefit_17b3()
        return b17b1.get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                              np.nan, np.nan, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_egl_min, x.pbp_b17b_coins_pct_egl_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_egl_min, x.pbp_b17b_copay_amt_egl_max)
                
class Benefit_17b4(Benefit_NMC):
    '''
    1 in 2	Contact lenses
    1 in 3	Eyeglasses (lenses and frames)
    1 in 4	Eyeglass lenses
    1 in 5	Eyeglass frames
    1 in 1	Upgrades
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 5
    BENEDESC_EHC_SERVICE = 5
    '''
    1 in 2	Medicare-covered Benefits
    1 in 3	Contact lenses
    1 in 4	Eyeglasses (lenses and frames)
    1 in 5	Eyeglass lenses
    1 in 6	Eyeglass frames
    1 in 1	Upgrades
    '''
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 6
    
    @staticmethod
    def get_INN_text(x):
        return Benefit_17b4().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn, 
                                              np.nan, np.nan, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_egf_min,x.pbp_b17b_coins_pct_egf_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_egf_min, x.pbp_b17b_copay_amt_egf_max)
        
class Benefit_17b5(Benefit_NMC):
    '''
    1 in 2	Contact lenses
    1 in 3	Eyeglasses (lenses and frames)
    1 in 4	Eyeglass lenses
    1 in 5	Eyeglass frames
    1 in 1	Upgrades
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 5
    BENEDESC_EHC_SERVICE = 1
    '''
    1 in 2	Medicare-covered Benefits
    1 in 3	Contact lenses
    1 in 4	Eyeglasses (lenses and frames)
    1 in 5	Eyeglass lenses
    1 in 6	Eyeglass frames
    1 in 1	Upgrades
    '''
    EHC_TOTAL_SERVICE = 6
    EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        return Benefit_17b5().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                              np.nan, np.nan, 
                                             x.pbp_b17b_bendesc_yn, x.pbp_b17b_bendesc_ehc,
    x.pbp_b17b_coins_yn,x.pbp_b17b_coins_ehc,x.pbp_b17b_coins_pct_upg_min, x.pbp_b17b_coins_pct_upg_max,
    x.pbp_b17b_copay_yn,x.pbp_b17b_copay_ehc,x.pbp_b17b_copay_amt_upg_min, x.pbp_b17b_copay_amt_upg_max)
  
class Benefit_18a(Benefit_MC_EHC):
    '''
    1 in 2	Medicare-covered Benefits
    1 in 3	Routine Hearing Exams
    1 in 1	Fitting/Evaluation for Hearing Aid
    '''
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 2

    @staticmethod
    def get_INN_text(x):
        inn_benefit = Benefit_18a().get_mc_ehc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                    x.pbp_b18a_copay_yn,x.pbp_b18a_copay_ehc, x.pbp_b18a_copay_amt, x.pbp_b18a_med_copay_amt_max,
                                                    x.pbp_b18a_coins_yn,x.pbp_b18a_coins_ehc, x.pbp_b18a_med_coins_pct, x.pbp_b18a_med_coins_pct_max)
        return inn_benefit

class Benefit_18a1(Benefit_NMC):
    
    '''
    1 in 2	Routine Hearing Exams
    1 in 1	Fitting/Evaluation for Hearing Aid
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 2
    BENEDESC_EHC_SERVICE = 2
    '''
    1 in 2	Medicare-covered Benefits
    1 in 3	Routine Hearing Exams
    1 in 1	Fitting/Evaluation for Hearing Aid
    '''
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 3

    @staticmethod
    def get_INN_text(x):        
        return Benefit_18a1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                       np.nan, np.nan,
                                                       x.pbp_b18a_bendesc_yn, x.pbp_b18a_bendesc_ehc,
                                                       x.pbp_b18a_coins_yn,x.pbp_b18a_coins_ehc,x.pbp_b18a_coins_pct_rht,x.pbp_b18a_coins_pct_max_rht,
                                                       x.pbp_b18a_copay_yn,x.pbp_b18a_copay_ehc,x.pbp_b18a_copay_amt_rht,x.pbp_b18a_copay_amt_max_rht)

class Benefit_18a2(Benefit_NMC):
    '''
    1 in 2	Routine Hearing Exams
    1 in 1	Fitting/Evaluation for Hearing Aid
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 2
    BENEDESC_EHC_SERVICE = 1
    '''
    1 in 2	Medicare-covered Benefits
    1 in 3	Routine Hearing Exams
    1 in 1	Fitting/Evaluation for Hearing Aid
    '''
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        return Benefit_18a2().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                       np.nan, np.nan,
                                             x.pbp_b18a_bendesc_yn, x.pbp_b18a_bendesc_ehc,
    x.pbp_b18a_coins_yn,x.pbp_b18a_coins_ehc,x.pbp_b18a_coins_pct_fha,x.pbp_b18a_coins_pct_max_fha,
    x.pbp_b18a_copay_yn,x.pbp_b18a_copay_ehc,x.pbp_b18a_copay_amt_fha,x.pbp_b18a_copay_amt_max_fha)
        
class Benefit_18b1(Benefit_NMC):
    '''
    1 in 2	Hearing Aids (all types)
    1 in 3	Hearing Aids - Inner Ear
    1 in 4	Hearing Aids - Outer Ear
    1 in 1	Hearing Aids - Over the Ear
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 4
    BENEDESC_EHC_SERVICE = 2
    '''
    1 in 2	Hearing Aids - Inner Ear
    1 in 3	Hearing Aids - Outer Ear
    1 in 1	Hearing Aids - Over the Ear
    '''
    EHC_TOTAL_SERVICE = np.nan
    EHC_SERVICE = np.nan
    
    @staticmethod
    def get_INN_text(x):
        return Benefit_18b1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                       np.nan, np.nan,
                                             x.pbp_b18b_bendesc_yn, x.pbp_b18b_bendesc_ehc,
    x.pbp_b18b_coins_yn,x.pbp_b18b_coins_ehc,x.pbp_b18b_coins_pct_at_min,x.pbp_b18b_coins_pct_at_max,
    x.pbp_b18b_copay_yn,x.pbp_b18b_copay_ehc,x.pbp_b18b_copay_at_min_amt,x.pbp_b18b_copay_at_max_amt)      
        
class Benefit_18b2(Benefit_NMC):
    '''
    1 in 2	Hearing Aids (all types)
    1 in 3	Hearing Aids - Inner Ear
    1 in 4	Hearing Aids - Outer Ear
    1 in 1	Hearing Aids - Over the Ear
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 4
    BENEDESC_EHC_SERVICE = 3
    '''
    1 in 2	Hearing Aids - Inner Ear
    1 in 3	Hearing Aids - Outer Ear
    1 in 1	Hearing Aids - Over the Ear
    '''
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 2
    
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_18b1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                       np.nan, np.nan,
                                             x.pbp_b18b_bendesc_yn, x.pbp_b18b_bendesc_ehc,
    x.pbp_b18b_coins_yn,x.pbp_b18b_coins_ehc,x.pbp_b18b_coins_pct_ie_min,x.pbp_b18b_coins_pct_ie_max,
    x.pbp_b18b_copay_yn,x.pbp_b18b_copay_ehc,x.pbp_b18b_copay_amt_per_ie_min,x.pbp_b18b_copay_amt_per_ie_max)      
        
        if x.pbp_b18b_bendesc_lim_ie == 2:
            benefit_text += f"<br/>Maximum {str(int(x.pbp_b18b_bendesc_numv_ie))} {Benefit_18b1().get_periodicity_text(x.pbp_b18b_bendesc_per_ie)}"
        return benefit_text
    
class Benefit_18b3(Benefit_NMC):
    '''
    1 in 2	Hearing Aids (all types)
    1 in 3	Hearing Aids - Inner Ear
    1 in 4	Hearing Aids - Outer Ear
    1 in 1	Hearing Aids - Over the Ear
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 4
    BENEDESC_EHC_SERVICE = 4
    '''
    1 in 2	Hearing Aids - Inner Ear
    1 in 3	Hearing Aids - Outer Ear
    1 in 1	Hearing Aids - Over the Ear
    '''
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 3
    
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_18b1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                       np.nan, np.nan,
                                             x.pbp_b18b_bendesc_yn, x.pbp_b18b_bendesc_ehc,
    x.pbp_b18b_coins_yn,x.pbp_b18b_coins_ehc,x.pbp_b18b_coins_pct_oe_min,x.pbp_b18b_coins_pct_oe_max,
    x.pbp_b18b_copay_yn,x.pbp_b18b_copay_ehc,x.pbp_b18b_copay_amt_per_oe_min,x.pbp_b18b_copay_amt_per_oe_max)      
        
        if x.pbp_b18b_bendesc_lim_oe == 2:
            benefit_text += f"<br/>Maximum {str(int(x.pbp_b18b_bendesc_numv_oe))} {Benefit_18b1().get_periodicity_text(x.pbp_b18b_bendesc_per_oe)}"
        return benefit_text
    
class Benefit_18b4(Benefit_NMC):
    '''
    1 in 2	Hearing Aids (all types)
    1 in 3	Hearing Aids - Inner Ear
    1 in 4	Hearing Aids - Outer Ear
    1 in 1	Hearing Aids - Over the Ear
    '''
    BENEDESC_EHC_TOTAL_SERVICE = 4
    BENEDESC_EHC_SERVICE = 1
    '''
    1 in 2	Hearing Aids - Inner Ear
    1 in 3	Hearing Aids - Outer Ear
    1 in 1	Hearing Aids - Over the Ear
    '''
    EHC_TOTAL_SERVICE = 3
    EHC_SERVICE = 1
    
    @staticmethod
    def get_INN_text(x):
        benefit_text = Benefit_18b1().get_nmc_inn_benefit_text(x.pbp_a_special_need_plan_type, x.pbp_a_dsnp_zerodollar, x.pbp_a_snp_state_cvg_yn,
                                                       np.nan, np.nan,
                                             x.pbp_b18b_bendesc_yn, x.pbp_b18b_bendesc_ehc,
    x.pbp_b18b_coins_yn,x.pbp_b18b_coins_ehc,x.pbp_b18b_coins_pct_ote_min,x.pbp_b18b_coins_pct_ote_max,
    x.pbp_b18b_copay_yn,x.pbp_b18b_copay_ehc,x.pbp_b18b_copay_amt_per_ote_min,x.pbp_b18b_copay_amt_per_ote_max)      
        
        if x.pbp_b18b_bendesc_lim_ote == 2:
            benefit_text += f"<br/>Maximum {str(int(x.pbp_b18b_bendesc_numv_ote))} {Benefit_18b1().get_periodicity_text(x.pbp_b18b_bendesc_per_ote)}"
        return benefit_text
    
    