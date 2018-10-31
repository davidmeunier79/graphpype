"""
Wrapper around radatools
"""
import os

# TODO should be done for PrepRada
from nipype.interfaces.base import CommandLine, CommandLineInputSpec
from nipype.interfaces.base import traits, File, TraitedSpec

from nipype.utils.filemanip import split_filename as split_f

# PrepRada


class PrepRadaInputSpec(CommandLineInputSpec):
    net_List_file = File(
        exists=True,
        desc='List of edges describing net in format i j weight',
        mandatory=True, position=0, argstr="%s")

    Pajek_net_file = File(
        desc="net description in Pajek format, generated by radatools",
        position=1, argstr="%s", name_source=['net_List_file'],
        hash_files=True, name_template='%s.net', keep_extension=False)

    network_type = traits.Enum(
        "A", "U", "D", usedefault=True,
        desc='Type of network, default A = "auto", U = force to undirected',
        position=2,
        argstr="%s")


class PrepRadaOutputSpec(TraitedSpec):

    Pajek_net_file = File(
        exists=True,
        desc="net description in Pajek format, generated by radatools")


class PrepRada(CommandLine):
    """
    Description:
        Format net list (format i j weight) to Pajek file
        wraps List_To_Net.exe from radatools

    Inputs:
        net_List_file:
            type = File, exists=True,
            desc='List of edges describing net in format i j weight',
            mandatory=True, position = 0, argstr = "%s"

        Pajek_net_file:
            type = File, desc="net description in Pajek format,
            generated by radatools",position = 1, argstr = "%s", name_source =
            ['net_List_file'], hash_files = True,
            name_template='%s.net',keep_extension = False

        network_type:
            type = traits.Enum("A","U","D", usedefault =True,
            desc='Type of network, force to undirected', position = 2,
            argstr="%s")

    Outputs:
        Pajek_net_file:
            type = File, exists=True,
            desc="net description in Pajek format, generated by radatools"

    """
    input_spec = PrepRadaInputSpec
    output_spec = PrepRadaOutputSpec

    _cmd = 'List_To_Net.exe'

    def _list_outputs(self):
        outputs = self._outputs().get()
        net_List_file = self.inputs.net_List_file
        path, fname, ext = split_f(net_List_file)
        outputs["Pajek_net_file"] = os.path.abspath(fname + '.net')
        return outputs

# NetPropRada


class NetPropRadaInputSpec(CommandLineInputSpec):

    Pajek_net_file = File(exists=True, desc='net description in Pajek format',
                          mandatory=True, position=0, argstr="%s")

    optim_seq = traits.String(
        'all 2', usedefault=True,
        desc="Optimisation sequence, see radatools documentation for more \
            information", position=1, argstr=" %s")


class NetPropRadaOutputSpec(TraitedSpec):
    # rada_log_file = File(
    #   exists=True,
    #   desc="network properties log, generated by radatools")
    pass


class NetPropRada(CommandLine):

    """
    Definition:

    Launch Network properties on Pajek file with given parameters
    (see Network_Properties in Radatools)

    Inputs:

        Pajek_net_file:
            type = File, exists=True, desc='net description in Pajek format',
            mandatory=True, position = 0, argstr = "%s"

        optim_seq:
            type String, default = 'all 2',usedefault = True,
            desc = "Optimisation sequence, see radatools documentation for
            more information", position = 1, argstr = " %s"

    Outputs:

        rada_log_file: (not used anymore)
            type = File, exists=True,
            desc="network properties log, generated by radatools"
    """
    # TODO: was previsously working in the "normal", nipype wrapping
    # commandline way, but failed with following versions

    input_spec = NetPropRadaInputSpec
    output_spec = NetPropRadaOutputSpec

    _cmd = 'Network_Properties.exe'

    def _run_interface(self, runtime):

        Pajek_net_file = self.inputs.Pajek_net_file
        optim_seq = self.inputs.optim_seq

        path, fname, ext = split_f(Pajek_net_file)
        rada_log_file = os.path.abspath(fname + '.log')

        cmd = 'Network_Properties.exe {} {} > {}'.format(Pajek_net_file,
                                                         optim_seq,
                                                         rada_log_file)

        os.system(cmd)

        return runtime

    def _list_outputs(self):

        outputs = self._outputs().get()
        path, fname, ext = split_f(self.inputs.Pajek_net_file)
        # outputs["rada_log_file"] = os.path.abspath(fname + '.log')
        return outputs

# CommRada


class CommRadaInputSpec(CommandLineInputSpec):

    optim_seq = traits.String(
        mandatory=True,
        desc="Optimisation sequence, see radatools documentation for more \
            information",
        position=0,
        argstr=" v %s")

    Pajek_net_file = File(
        exists=True,
        desc='net description in Pajek format',
        mandatory=True,
        position=1,
        argstr=" %s")

    rada_lol_file = File(
        desc="modularity structure description, generated by radatools",
        position=2,
        argstr=" %s",
        name_source=['Pajek_net_file'],
        hash_files=True,
        name_template='%s.lol',
        keep_extension=False)

    rada_log_file = File(
        desc="modularity structure description, generated by radatools",
        position=3,
        argstr=" > %s",
        name_source=['Pajek_net_file'],
        hash_files=True,
        name_template='%s.log',
        keep_extension=False)


class CommRadaOutputSpec(TraitedSpec):

    rada_lol_file = File(
        exists=True,
        desc="modularity structure description, generated by radatools")

    rada_log_file = File(
        exists=True,
        desc="optimisation steps, generated by radatools")

    lol_log_file = File(
        exists=True,
        desc="different optimisation steps, generated by radatools")


class CommRada(CommandLine):

    """
    Description:

    (The big one :)

    Launch community detection on Pajek file with given optimisation args

    Inputs:

        optim_seq:
            type = String, mandatory = True,
            desc = "Optimisation sequence, see radatools documentation for
            more information",
            position = 0, argstr = " v %s"

        Pajek_net_file:
            type = File, exists=True, desc='net description in Pajek format',
            mandatory=True, position = 1, argstr = " %s"

        rada_lol_file:
            type = File,
            desc="modularity structure description, generated by
            radatools",
            position = 2,
            argstr = " %s",
            name_source = ['Pajek_net_file'],
            hash_files = True,
            name_template='%s.lol',
            keep_extension = False

        rada_log_file:
            type = File,
            desc="modularity structure description, generated by radatools",
            position = 3, argstr = " > %s",
            name_source = ['Pajek_net_file'],
            hash_files = True,
            name_template='%s.log',
            keep_extension = False

    Outputs:

        rada_lol_file
            type = File, exists=True,
            desc="modularity structure description, generated by radatools"

        rada_log_file
            type = File, exists=True,
            desc="optimisation steps, generated by radatools"
    """

    input_spec = CommRadaInputSpec
    output_spec = CommRadaOutputSpec

    _cmd = "Communities_Detection.exe"

    def _list_outputs(self):

        outputs = self._outputs().get()

        path, fname, ext = split_f(self.inputs.Pajek_net_file)

        outputs["rada_lol_file"] = os.path.abspath(fname + '.lol')
        outputs["rada_log_file"] = os.path.abspath(fname + '.log')
        outputs["lol_log_file"] = os.path.abspath(fname + '.lol.log')

        return outputs
