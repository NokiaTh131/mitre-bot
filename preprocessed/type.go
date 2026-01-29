package main

type AttackPattern struct {
	ID          string   `json:"id"`
	Name        string   `json:"name"`
	Description string   `json:"description"`
	Platforms   []string `json:"platforms"`
}

type Bundle struct {
	Type        string       `json:"type"`
	ID          string       `json:"id"`
	SpecVersion string       `json:"spec_version"`
	Objects     []STIXObject `json:"objects"`
}

type STIXObject struct {
	Type               string              `json:"type"`
	ID                 string              `json:"id"`
	Created            string              `json:"created,omitempty"`
	Modified           string              `json:"modified,omitempty"`
	CreatedByRef       string              `json:"created_by_ref,omitempty"`
	Revoked            bool                `json:"revoked,omitempty"`
	Name               string              `json:"name,omitempty"`
	Description        string              `json:"description,omitempty"`
	ExternalReferences []ExternalReference `json:"external_references,omitempty"`
	ObjectMarkingRefs  []string            `json:"object_marking_refs,omitempty"`
	KillChainPhases    []KillChainPhase    `json:"kill_chain_phases,omitempty"`

	// MITRE-specific extensions
	XMitreAttackSpecVersion string   `json:"x_mitre_attack_spec_version,omitempty"`
	XMitreContributors      []string `json:"x_mitre_contributors,omitempty"`
	XMitreDeprecated        bool     `json:"x_mitre_deprecated,omitempty"`
	XMitreDetection         string   `json:"x_mitre_detection,omitempty"`
	XMitreDomains           []string `json:"x_mitre_domains,omitempty"`
	XMitreIsSubtechnique    bool     `json:"x_mitre_is_subtechnique,omitempty"`
	XMitreModifiedByRef     string   `json:"x_mitre_modified_by_ref,omitempty"`
	XMitrePlatforms         []string `json:"x_mitre_platforms,omitempty"`
	XMitreVersion           string   `json:"x_mitre_version,omitempty"`
}

type ExternalReference struct {
	SourceName  string `json:"source_name"`
	Description string `json:"description,omitempty"`
	URL         string `json:"url,omitempty"`
	ExternalID  string `json:"external_id,omitempty"`
}

type KillChainPhase struct {
	KillChainName string `json:"kill_chain_name"`
	PhaseName     string `json:"phase_name"`
}
