package app

import (
	"github.com/pachirode/pkg/log"
	"github.com/pachirode/pkg/version"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"

	"github.com/pachirode/ffmpeg-study/cmd/apiserver/app/options"
)

var configFile string

func NewServerCommand() *cobra.Command {
	opts := options.NewServerOptions()

	cmd := &cobra.Command{
		Use:          "server-apiserver",
		Short:        "A server for ffmpeg",
		SilenceUsage: true,
		RunE: func(cmd *cobra.Command, args []string) error {
			return run(opts)
		},
		Args: cobra.NoArgs,
	}

	cobra.OnInitialize(onInitialize)
	cmd.PersistentFlags().StringVarP(&configFile, "config", "c", filePath(), "Path to the configuration file.")
	opts.AddFlags(cmd.PersistentFlags())
	version.AddFlags(cmd.PersistentFlags())

	return cmd
}

func run(opts *options.ServerOptions) error {
	version.PrintAndExitIfRequested()
	log.Init(logOptions())
	defer log.Sync()

	if err := viper.Unmarshal(opts); err != nil {
		return err
	}

	// 校验命令行选项
	if err := opts.Validate(); err != nil {
		return err
	}

	// 获取应用配置.
	// 将命令行选项和应用配置分开，可以更加灵活的处理 2 种不同类型的配置.
	cfg, err := opts.Config()
	if err != nil {
		return err
	}

	// 创建服务器实例.
	// 注意这里是联合服务器，因为可能同时启动多个不同类型的服务器.
	server, err := cfg.NewUnionServer()
	if err != nil {
		return err
	}

	// 启动服务器
	return server.Run()
}

func logOptions() *log.Options {
	opts := log.NewOptions()
	if viper.IsSet("log.disable-caller") {
		opts.DisableCaller = viper.GetBool("log.disable-caller")
	}
	if viper.IsSet("log.disable-stacktrace") {
		opts.DisableStacktrace = viper.GetBool("log.disable-stacktrace")
	}
	if viper.IsSet("log.level") {
		opts.Level = viper.GetString("log.level")
	}
	if viper.IsSet("log.format") {
		opts.Format = viper.GetString("log.format")
	}
	if viper.IsSet("log.output-paths") {
		opts.OutputPaths = viper.GetStringSlice("log.output-paths")
	}
	return opts
}
