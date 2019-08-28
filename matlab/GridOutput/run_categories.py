categories2 = {
    'default':
        {'description': "Run with default settings",
         'runnumbers': [[81, 107, 108], [52]]
         },
    'fixed_feedback_inhibitory':
        {'description': "Runs only with feedback to inhibitory cells",
         'runnumbers': [[81, 107, 108], [127, 154], [106, 104, 152], [130, 151], [105, 155], [71], [80], [70], [69], [68]]
         },
    'fixed_feedback_excitatory_inhibitory':
         {'description': "Runs with feedback to excitatory and inhibitory cells",
         'runnumbers': [[146], [149], [147], [150]]
         },
    'information_brown_fixed_feedback_inhibitory':
        {
            'description': "Noiseamp = 1: Runs concerned with information transfer with feedback to inhibitory cells. Using Brown noise!",
            'runnumbers': [[117, 125], [124], [118], [122]]
        },
    'information_feedback_inhibitory_weak_brown_results_figures':
        {
            'description': "Runnumbers used for results section of thesis, with noiseseed [46, 80] for each entry. Uses noiseamp=0.5 brownian noise and inhibitory feedback [0, 0.025, 0.05, 0.075, 0.1]",
            'runnumbers': [[140, 134], [141, 135], [142, 136], [132, 138], [133, 139]]
        },
    'information_brown_fixed_feedback_inhibitory_noiseamp_low':
        {
            'description': "Noiseamp = 0.5 - Runs concerned with information transfer with feedback to inhibitory cells. Using Brown noise! Caution: Run 95 has noiseamp = 0.5",
            'runnumbers': [[140, 134, 95, 126], [141, 135, 128], [142, 136, 129], [132, 138], [133, 139]]
        },
    'information_pink_fixed_feedback_inhibitory':
        {
            'description': "Caution: Using Pink Noise! Runs concerned with information transfer with feedback to inhibitory cells",
            'runnumbers': [[112, 115], [114], [113], [116]]
        },
    'information_white_fixed_feedback_inhibitory':
        {
            'description': "Caution: Using Pink Noise! Runs concerned with information transfer with feedback to inhibitory cells",
            'runnumbers': [[123]]
        },
    'explore_delay':
        {'description': "Runs to explore what happens when we introduce delay",
         'runnumbers': [[79]]}
}

categories = {
    'feedforward_fixed_feedback':
        {'description': 'Runs, iterating over feedforward connections with fixed feedback connections',
         'runnumbers': [81, 106, 108, 52, 37, 38, 65, 66, 35, 55, 36, 67]},
    'feedforward_fixed_inhibitory_feedback':
        {
            'description': 'Runs, iterating over feedforward connections with fixed inhibitory feedback-connections (pyramidals projecting only to inhibitory cells)',
            'runnumbers': [52, 103, 107, 108, 70, 69, 106, 68, 71, 80]},
    'feedforward_fixed_excitatory_feedback':
        {
            'description': 'Runs, iterating over feedforward connections with fixed excitatory feedback-connections (pyramidals projecting only to pyramidal)',
            'runnumbers': [43]},
    'feedforward_inhibitory_information_transfer':
        {'description': 'Runs with inhibitory feedback with information transfer measures',
         'runnumbers': [112, 113, 77, 95, 89, 96, 90, 98, 87, 91, 97, 83]},
    'feedforward_exc_inh_information_transfer':
        {'description': 'Runs with exc. and inh. feedback with information transfer measures',
         'runnumbers': [77, 92, 84, 93]},
    'transient_oscillations':
        {'description': "Runs to explore how and why transient oscillations occur",
         'runnumbers': [38, 78, 82, 85, 86]},
    'feedback_fixed_feedforward':
        {'description': "Fixing the feedforward-connection, while iterating over feedback",
         'runnumbers': [56, 46, 47, 57]},
    'explore_delay':
        {
            'description': "Runs to explore what an increased delay does to effective delay measurements. Runs 77 and 110 are to compare what happens with information transfer delay with increased feedback",
            'runnumbers': [81, 79, 77]},
}

# This is supposed to become a set
excludes = set(range(333, 390))
