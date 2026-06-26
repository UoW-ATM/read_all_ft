# HEADERS OF DDR2 AND DDR3 FILES

def ddr_headers():
    h_ddrv2 = ['origin', 'destination', 'ac_id', 'operator', 'ac_type', 'aobt', 'ifps_id', 'iobt',
               'original_flight_data_quality', 'flight_data_quality', 'source', 'excemption_reason_type',
               'excemption_reason_distance', 'late_filer', 'late_updater', 'north_atlantic_flight_status',
               'cobt', 'eobt', 'lobt', 'flight_state', 'prev_to_activation_flight_state', 'suspension_status',
               'tact_id', 'sam_ctot', 'sam_sent', 'sip_ctot', 'sip_sent', 'slot_forced', 'most_penalising_reg_sid',
               'regulations_affected_by_nr_of_instances', 'reg_excluded_from_nr_of_instances',
               'last_received_atfm_message_title', 'last_received_message_title', 'last_sent_atfm_message_title',
               'manual_exemption_reason', 'sensitive_flight', 'ready_for_improvement', 'ready_to_depart',
               'revised_taxi_time', 'tis', 'trs', 'to_be_sent_slot_message_title', 'to_be_sent_proposal_message_title',
               'last_sent_slot_message_title', 'last_sent_proposal_message_title', 'last_sent_proposal_message',
               'last_sent_slot_message', 'flight_count_option', 'normal_flight_tact_id', 'proposal_flight_tact_id',
               'operating_aircraft_operator_icao_id', 'rerouting_why', 'rerouted_flight_state', 'runway_visual_range',
               'number_ignored_errors', 'arc_addr_source', 'arc_addr', 'ifps_registration_mark', 'flight_type_icao',
               'aircraft_equipment', 'cdm_status', 'cdm_early_ttot', 'cdm_ao_ttot', 'cdm_atc_ttot',
               'cdm_sequenced_ttot',
               'cdm_taxi_time', 'cdm_off_block_time_discrepancy', 'cdm_departure_procedure_id', 'cdm_aircraft_type_id',
               'cdm_registration_mark', 'cdm_no_slot_before', 'cdm_departure_status',
               'ftfmEetFirNrOfInstances', 'ftfmEetFirList', 'ftfmEetPtNrOfInstances', 'ftfmEetPtList',
               'ftfmAiracCycleRelease', 'ftfmEvnBaselineNumber', 'ftfmDepRunway', 'ftfmArrRunway',
               'ftfmReqFLSpeedNrInstances',
               'ftfmReqFLSpeedList']

    h_ddrv3 = h_ddrv2 + ['ftfmConsumedFuel', 'ftfmRouteCharges']

    h_ddrv2_cont = ['ftfmAllFtPointNrInstances', 'ftfmAllFtPointProfile', 'ftfmAirspNrInstances', 'ftfmAirspProfile',
                    'ftfmAllFtCircleIntersectionsNrInstances', 'ftfmAllFtCircleIntersections',
                    'rtfmAiracCycleRelease', 'rtfmEvnBaselineNumber', 'rtfmDepRunway', 'rtfmArrRunway',
                    'rtfmReqFLSpeedNrInstances',
                    'rtfmReqFLSpeedList']

    h_ddrv3 = h_ddrv3 + h_ddrv2_cont + ['rtfmConsumedFuel', 'rtfmRouteCharges']

    h_ddrv2 = h_ddrv2 + h_ddrv2_cont

    h_ddrv2_cont = ['rtfmAllFtPointNrInstances', 'rtfmAllFtPointProfile', 'rtfmAirspNrInstances', 'rtfmAirspProfile',
                    'rtfmAllFtCircleIntersectionsNrInstances', 'rtfmAllFtCircleIntersections',
                    'ctfmAiracCycleRelease', 'ctfmEvnBaselineNumber', 'ctfmDepRunway', 'ctfmArrRunway',
                    'ctfmReqFLSpeedNrInstances',
                    'ctfmReqFLSpeedList'
                    ]

    h_ddrv2 = h_ddrv2 + h_ddrv2_cont
    h_ddrv3 = h_ddrv3 + h_ddrv2_cont + ['ctfmConsumedFuel', 'ctfmRouteCharges']

    h_ddrv2_cont = ['ctfmAllFtPointNrInstances', 'ctfmAllFtPointProfile', 'ctfmAirspNrInstances', 'ctfmAirspProfile',
                    'ctfmAllFtCircleIntersectionsNrInstances', 'ctfmAllFtCircleIntersections',
                    'no_cpgcpf_reason']

    h_ddrv2 = h_ddrv2 + h_ddrv2_cont
    h_ddrv3 = h_ddrv3 + h_ddrv2_cont + ['scrObt', 'scrConsumedFuel', 'scrRouteCharges']

    h_ddrv2_cont = ['scrAllFtPointNrInstances', 'scrAllFtPointProfile', 'scrAirspNrInstances', 'scrAirspProfile',
                    'scrAllFtCircleIntersectionsNrInstances', 'scrAllFtCircleIntersections']

    h_ddrv2 = h_ddrv2 + h_ddrv2_cont
    h_ddrv3 = h_ddrv3 + h_ddrv2_cont + ['srrObt', 'srrConsumedFuel', 'srrRouteCharges']

    h_ddrv2_cont = ['srrAllFtPointNrInstances', 'srrAllFtPointProfile', 'srrAirspNrInstances', 'srrAirspProfile',
                    'srrAllFtCircleIntersectionsNrInstances', 'srrAllFtCircleIntersections']

    h_ddrv2 = h_ddrv2 + h_ddrv2_cont
    h_ddrv3 = h_ddrv3 + h_ddrv2_cont + ['surObt', 'surConsumedFuel', 'surRouteCharges']

    h_ddrv2_cont = ['surAllFtPointNrInstances', 'surAllFtPointProfile', 'surAirspNrInstances', 'surAirspProfile',
                    'surAllFtCircleIntersectionsNrInstances', 'surAllFtCircleIntersections']

    h_ddrv2 = h_ddrv2 + h_ddrv2_cont
    h_ddrv3 = h_ddrv3 + h_ddrv2_cont + ['dctObt', 'dctConsumedFuel', 'dctRouteCharges']

    h_ddrv2_cont = ['dctAllFtPointNrInstances', 'dctAllFtPointProfile', 'dctAirspNrInstances', 'dctAirspProfile',
                    'dctAllFtCircleIntersectionsNrInstances', 'dctAllFtCircleIntersections']

    h_ddrv2 = h_ddrv2 + h_ddrv2_cont
    h_ddrv3 = h_ddrv3 + h_ddrv2_cont + ['cpfObt', 'cpfConsumedFuel', 'cpfRouteCharges']

    h_ddrv2_cont = ['cpfAllFtPointNrInstances', 'cpfAllFtPointProfile', 'cpfAirspNrInstances', 'cpfAirspProfile',
                    'cpfAllFtCircleIntersectionsNrInstances', 'cpfAllFtCircleIntersections']

    h_ddrv2 = h_ddrv2 + h_ddrv2_cont
    h_ddrv3 = h_ddrv3 + h_ddrv2_cont

    h_ddrv2_cont = ['ac_id_iata', 'intention_flight', 'intention_related_route_assignment_method', 'intention_uid',
                    'intention_edition_date', 'intention_source', 'associated_intetions', 'enrichment_output']

    h_ddrv2 = h_ddrv2 + h_ddrv2_cont
    h_ddrv3 = h_ddrv3 + h_ddrv2_cont

    h_ddrv4 = h_ddrv3 + ['eventID', 'eventTime', 'flightVersionNr', 'ftfmNrTvProfiles', 'ftfmTvProfile',
                         'rtfmNrTvProfiles', 'rtfmTvProfile', 'ctfmNrTvProfiles', 'ctfmTvProfile']

    h_ddrv6 = h_ddrv4 + ['atfmDelay', 'atfmDelayTotRequested', 'atfmDelayTotRequestedOrigin',
                         'atfmDelayTotAllocated', 'atfmDelayTotAllocatedOrigin', 'atfmDelayTotTaxiTime',
                         'atfmDelayTotTaxiSource',
                         'adjustedToClock']
    h_ddrv8 = ['origin', 'destination', 'ac_id', 'operator', 'ac_type', 'aobt', 'ifps_id', 'iobt',
               'original_flight_data_quality',
               'flight_data_quality', 'source',
               'excemption_reason_type', 'excemption_reason_distance', 'late_filer', 'late_updater',
               'north_atlantic_flight_status', 'cobt', 'eobt', 'lobt',
               'flight_state', 'prev_to_activation_flight_state', 'suspension_status', 'tact_id', 'sam_ctot',
               'sam_sent', 'sip_ctot', 'sip_sent', 'slot_forced',
               'most_penalising_reg_sid', 'regulations_affected_by_nr_of_instances',
               'reg_excluded_from_nr_of_instances', 'last_received_atfm_message_title',
               'last_received_message_title', 'last_sent_atfm_message_title', 'manual_exemption_reason',
               'sensitive_flight', 'ready_for_improvement', 'ready_to_depart',
               'revised_taxi_time', 'tis', 'trs', 'to_be_sent_slot_message_title', 'to_be_sent_proposal_message_title',
               'last_sent_slot_message_title',
               'last_sent_proposal_message_title', 'last_sent_proposal_message', 'last_sent_slot_message',
               'flight_count_option', 'normal_flight_tact_id',
               'proposal_flight_tact_id', 'operating_aircraft_operator_icao_id', 'rerouting_why',
               'rerouted_flight_state', 'runway_visual_range',
               'number_ignored_errors', 'arc_addr_source', 'arc_addr', 'ifps_registration_mark', 'flight_type_icao',
               'aircraft_equipment', 'cdm_status',
               'cdm_early_ttot', 'cdm_ao_ttot', 'cdm_atc_ttot', 'cdm_sequenced_ttot', 'cdm_taxi_time',
               'cdm_off_block_time_discrepancy', 'cdm_departure_procedure_id',
               'cdm_aircraft_type_id', 'cdm_registration_mark', 'cdm_no_slot_before', 'cdm_departure_status',
               'ftfmEetFirNrOfInstances', 'ftfmEetFirList',
               'ftfmEetPtNrOfInstances', 'ftfmEetPtList', 'ftfmAiracCycleRelease', 'ftfmEvnBaselineNumber',
               'ftfmDepRunway', 'ftfmArrRunway',
               'ftfmReqFLSpeedNrInstances', 'ftfmReqFLSpeedList', 'ftfmConsumedFuel', 'ftfmRouteCharges',
               'ftfmAllFtPointNrInstances', 'ftfmAllFtPointProfile',
               'ftfmAirspNrInstances', 'ftfmAirspProfile', 'ftfmAllFtFuelBurnProfileNrInstances',
               'ftfmAllFtFuelBurnProfile', 'ftfmAllFtCircleIntersectionsNrInstances',
               'ftfmAllFtCircleIntersections', 'rtfmAiracCycleRelease', 'rtfmEvnBaselineNumber', 'rtfmDepRunway',
               'rtfmArrRunway', 'rtfmReqFLSpeedNrInstances',
               'rtfmReqFLSpeedList', 'rtfmConsumedFuel', 'rtfmRouteCharges', 'rtfmAllFtPointNrInstances',
               'rtfmAllFtPointProfile', 'rtfmAirspNrInstances',
               'rtfmAirspProfile', 'rtfmAllFtFuelBurnProfileNrOfInstances', 'rtfmAllFtFuelBurnProfile',
               'rtfmAllFtCircleIntersectionsNrInstances',
               'rtfmAllFtCircleIntersections', 'ctfmAiracCycleRelease', 'ctfmEvnBaselineNumber', 'ctfmDepRunway',
               'ctfmArrRunway', 'ctfmReqFLSpeedNrInstances',
               'ctfmReqFLSpeedList', 'ctfmConsumedFuel', 'ctfmRouteCharges', 'ctfmAllFtPointNrInstances',
               'ctfmAllFtPointProfile', 'ctfmAirspNrInstances',
               'ctfmAirspProfile', 'ctfmAllFtFuelBurnProfileNrOfInstances', 'ctfmAllFtFuelBurnProfile',
               'ctfmAllFtCircleIntersectionsNrInstances',
               'ctfmAllFtCircleIntersections', 'no_cpgcpf_reason', 'scrObt', 'scrConsumedFuel', 'scrRouteCharges',
               'scrAllFtPointNrInstances', 'scrAllFtPointProfile',
               'scrAirspNrInstances', 'scrAirspProfile', 'scrAllFtFuelBurnProfileNrOfInstances',
               'scrAllFtFuelBurnProfile', 'scrAllFtCircleIntersectionsNrInstances',
               'scrAllFtCircleIntersections', 'srrObt', 'srrConsumedFuel', 'srrRouteCharges',
               'srrAllFtPointNrInstances', 'srrAllFtPointProfile', 'srrAirspNrInstances',
               'srrAirspProfile', 'srrAllFtFuelBurnProfileNrOfInstances', 'srrAllFtFuelBurnProfile ',
               'srrAllFtCircleIntersectionsNrInstances',
               'srrAllFtCircleIntersections', 'surObt', 'surConsumedFuel', 'surRouteCharges',
               'surAllFtPointNrInstances', 'surAllFtPointProfile', 'surAirspNrInstances',
               'surAirspProfile', 'surAllFtFuelBurnProfileNrOfInstances', 'surAllFtFuelBurnProfile',
               'surAllFtCircleIntersectionsNrInstances',
               'surAllFtCircleIntersections', 'dctObt', 'dctConsumedFuel', 'dctRouteCharges',
               'dctAllFtPointNrInstances', 'dctAllFtPointProfile', 'dctAirspNrInstances',
               'dctAirspProfile', 'dctAllFtFuelBurnProfileNrOfInstances', 'dctAllFtFuelBurnProfile',
               'dctAllFtCircleIntersectionsNrInstances',
               'dctAllFtCircleIntersections', 'cpfObt', 'cpfConsumedFuel', 'cpfRouteCharges',
               'cpfAllFtPointNrInstances', 'cpfAllFtPointProfile', 'cpfAirspNrInstances',
               'cpfAirspProfile', 'cpfAllFtFuelBurnProfileNrOfInstances', 'cpfAllFtFuelBurnProfile',
               'cpfAllFtCircleIntersectionsNrInstances',
               'cpfAllFtCircleIntersections', 'ac_id_iata', 'intention_flight',
               'intention_related_route_assignment_method', 'intention_uid', 'intention_edition_date',
               'intention_source', 'associated_intetions', 'enrichment_output', 'eventID', 'eventTime',
               'flightVersionNr', 'ftfmNrTvProfiles', 'ftfmTvProfile',
               'rtfmNrTvProfiles', 'rtfmTvProfile', 'ctfmNrTvProfiles', 'ctfmTvProfile', 'atfmDelay',
               'atfmDelayTotRequested', 'atfmDelayTotRequestedOrigin',
               'atfmDelayTotAllocated', 'atfmDelayTotAllocatedOrigin', 'atfmDelayTotTaxiTime', 'atfmDelayTotTaxiSource',
               'adjustedToClock', 'alternateAerodrome1',
               'alternateAerodrome2', 'ntfmField15', 'ftfmField15', 'rtfmField15', 'ctfmField15', 'wakeTcategory',
               'initialFlightRules', 'remark', ]

    return h_ddrv2, h_ddrv3, h_ddrv4, h_ddrv6, h_ddrv8
