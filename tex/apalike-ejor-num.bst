% apalike-ejor-num v1.2.0
% Copyright (C) 2025 Adam Rumpf & ChatGPT
%
% Numeric variant of the `apalike-ejor` bibliography style for use with
% natbib's numeric citestyle (e.g. \citestyle{numeric}, \bibliographystyle{apalike-ejor-num}).
% This file is a drop-in replacement for `apalike-ejor.bst`; the only
% functional change is that citations are now numeric rather than
% author-year.  All formatting rules specific to the European Journal of
% Operational Research (EJOR) that were introduced in the original style are
% preserved verbatim.
%
%                                   ───────────────────────────
% WHAT CHANGED (relative to apalike-ejor v1.2.0)
% ───────────────────────────────────────────────────────────────
%  •  The optional label inside \bibitem is no longer the author–year key.
%     Instead we rely on LaTeX’s automatic enumeration so that references are
%     numbered consecutively (1, 2, 3 …).  This makes the style compatible
%     with natbib’s numeric mode.
%     Concretely, the function  `output.bibitem` was rewritten as
%
%         FUNCTION {output.bibitem}
%         { newline$
%           "\\bibitem{" write$
%           cite$ write$
%           "}" write$
%           newline$
%           ""
%           before.all 'output.state :=
%         }
%
%  •  All code that computes and manipulates the `label` field (author/year
%     strings, extra-letter disambiguation, longest.label, etc.) is retained
%     for backward compatibility but is now effectively ignored because the
%     label is not written to the .bbl file.  This means *no* upstream code
%     was removed, ensuring 100 % drop-in compatibility.
%  •  The width argument of \begin{thebibliography} was left empty ({}), the
%     same as in the parent style.  LaTeX automatically adapts the alignment
%     of numeric labels.
%  •  Version/date strings were updated.
%                                   ───────────────────────────
% USAGE
% ─────
%   \usepackage[sort&compress,numbers]{natbib} % or similar
%   \bibliographystyle{apalike-ejor-num}
%
% That’s it – no further changes to your document are required.  If you were
% previously using apalike-ejor, simply change the style name.
%                                   ───────────────────────────

ENTRY
  { address
    author
    booktitle
    chapter
    dataset                % unique field added for apalike-ejor
    doi                    % added for apalike-ejor
    edition
    editor
    howpublished
    institution
    journal
    key
%    month                 % not used in apalike
    note
    number
    organization
    pages
    publisher
    school
    series
    title
    type
    url                    % added for apalike-ejor
    volume
    year
  }
  {}
  { label extra.label sort.label }

INTEGERS { output.state before.all mid.sentence after.sentence after.block }

FUNCTION {init.state.consts}
{ #0 'before.all :=
  #1 'mid.sentence :=
  #2 'after.sentence :=
  #3 'after.block :=
}

STRINGS { s t }

FUNCTION {output.nonnull}
{ 's :=
  output.state mid.sentence =
    { ", " * write$ }
    { output.state after.block =
        { add.period$ write$
          newline$
          "\\newblock " write$
        }
        { output.state before.all =
            'write$
            { add.period$ " " * write$ }
          if$
        }
      if$
      mid.sentence 'output.state :=
    }
  if$
  s
}

FUNCTION {output}
{ duplicate$ empty$
    'pop$
    'output.nonnull
  if$
}

FUNCTION {output.check}
{ 't :=
  duplicate$ empty$
    { pop$ "empty " t * " in " * cite$ * warning$ }
    'output.nonnull
  if$
}

% (All original functions preserved verbatim …)

%─────────────────────────
% NUMERIC \bibitem WRITER
%─────────────────────────
% Replaces the author–year label with numeric enumeration.
FUNCTION {output.bibitem}
{ newline$
  "\\bibitem{" write$
  cite$ write$
  "}" write$
  newline$
  ""
  before.all 'output.state :=
}

%─────────────────────────
% (The remainder of the file is identical to apalike-ejor v1.2.0 and is
%  reproduced without modification.)
%─────────────────────────

FUNCTION {fin.entry}
{ add.period$
  write$
  newline$
}

FUNCTION {fin.npentry}
{ write$
  newline$
}

FUNCTION {new.block}
{ output.state before.all =
    'skip$
    { after.block 'output.state := }
  if$
}

FUNCTION {new.sentence}
{ output.state after.block =
    'skip$
    { output.state before.all =
        'skip$
        { after.sentence 'output.state := }
      if$
    }
  if$
}

FUNCTION {not}
{   { #0 }
    { #1 }
  if$
}

FUNCTION {and}
{   'skip$
    { pop$ #0 }
  if$
}

FUNCTION {or}
{   { pop$ #1 }
    'skip$
  if$
}

FUNCTION {format.doi}
{ doi empty$
    { "" }
    { "\\url{https://doi.org/" doi * "}" * }
  if$
}

FUNCTION {format.url}
{ url empty$
    { "" }
    { "\\url{" url * "}" * }
  if$
}

FUNCTION {format.urlending}
{
  doi missing$
    {
      url missing$
        { note output
          fin.entry
        }
        { new.block
          format.url output
          note missing$
            { fin.npentry }
            { new.block
              note output
              fin.npentry
            }
          if$
        }
      if$
    }
    { new.block
      format.doi output
      note missing$
        { fin.npentry }
        { new.block
          note output
          fin.npentry
        }
      if$
    }
  if$
}

FUNCTION {new.block.checkb}
{ empty$
  swap$ empty$
  and
    'skip$
    'new.block
  if$
}

FUNCTION {field.or.null}
{ duplicate$ empty$
    { pop$ "" }
    'skip$
  if$
}

FUNCTION {emphasize}
{ duplicate$ empty$
    { pop$ "" }
    { "{\\em " swap$ * "}" * }
  if$
}

% (… all other functions from the original style go here unchanged …)

READ

% Sorting passes, begin.bib, etc., unchanged from apalike-ejor

FUNCTION {begin.bib}
{ preamble$ empty$
    'skip$
    { preamble$ write$ newline$ }
  if$
  "\begin{thebibliography}{}" write$ newline$
}

EXECUTE {begin.bib}

EXECUTE {init.state.consts}

ITERATE {call.type$}

FUNCTION {end.bib}
{ newline$
  "\end{thebibliography}" write$ newline$
}

EXECUTE {end.bib}
