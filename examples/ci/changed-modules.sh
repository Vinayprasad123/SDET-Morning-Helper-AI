#!/usr/bin/env bash
# Map changed files to pod-wise Jenkins modules. Framework-level changes → "All Modules" (Smoke).
base=${1:-origin/master}
changed=$(git diff --name-only "$base"...HEAD)

declare -A POD=(
  [Campaigns]="SMSCampaigns,EmailCampaigns,PushCampaigns,WebPushCampaign,Whatsapp,RCSCampaigns,ViberCampaigns,InAppCampaigns"
  [Journeys]="Journeys,Relays"
  [Personalisation]="OnsiteNotification,InLineContentWebP,InLineContentAppP,MessagePersonalisation,Catalogs,Recommendations"
  [Data]="Users,LiveSegments,StaticSegments,CustomEntity,DerivedAttributes"
  [Analytics]="EventAnalyticsCore1,EventAnalyticsCore2,Funnels,CustomDashboard,CustomAlerts"
)

if echo "$changed" | grep -qE '/(utils|hooks|runners|initialize)/|pom\.xml'; then
  echo "All Modules"; exit 0
fi

modules=""
for pod in "${!POD[@]}"; do
  for m in ${POD[$pod]//,/ }; do
    if echo "$changed" | grep -qi "$m"; then modules+="${POD[$pod]},"; break; fi
  done
done
modules=$(echo "${modules%,}" | tr ',' '\n' | sort -u | paste -sd, -)
echo "${modules:-All Modules}"
