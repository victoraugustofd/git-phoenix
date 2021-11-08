_git_phoenix() {
  __core
}

_git_px() {
  __core
}

__core() {
  local template=$(git config --get phoenix.template.path)
  local list=""

  if [ -z $template ]; then
    case $prev in
    help) ;;

    *)
      list="help"
      ;;
    esac
  else
    case $prev in
    phoenix | px)
      local commands=$(jq -cr '.commands | map(.name) | join(" ")' <<<$(jq -cr . $template))
      list="$commands"
      ;;
    *)
      local wordCount=${#COMP_WORDS[@]}

      if [ "$wordCount" -le 4 ]; then
        list=$(jq -cr --arg COMMAND $prev '.commands[] | select(.name == $COMMAND) | .actions | map(.name) | join(" ")' <<<$(jq -c . $template))
      else
        local pattern_to_search=""
        local command=${COMP_WORDS[2]}
        local action=${COMP_WORDS[3]}
        local subaction=$(jq -cr --arg COMMAND $command --arg ACTION $action '[.commands[] | select(.name == $COMMAND) | .actions[] | select(.name == $ACTION) | .execution[] | .do | .action][0]' <<<$(jq -c . $template))

        case $subaction in
        create_branch)
          pattern_to_search="pattern_example"
          ;;
        merge)
          pattern_to_search="origin_pattern"
          ;;
        esac

        local pattern=$(jq -cr --arg COMMAND $command --arg ACTION $action --arg SUBACTION $subaction --arg PATTERN $pattern_to_search '.commands[] | select(.name == $COMMAND) | .actions[] | select(.name == $ACTION) | .execution[] | .do | select(.action == $SUBACTION) | .parameters | .[$PATTERN]' <<<$(jq -c . $template))

        case $subaction in
        create_branch)
          list=$pattern
          ;;
        merge)
          #pattern=__change_value $pattern
          list=$(git for-each-ref --format='%(refname:short)' refs/heads | grep ^"$pattern")
          ;;
        esac

      fi
      ;;
    esac
  fi

  __gitcomp "$list"
}

__change_value() {
  echo
}
